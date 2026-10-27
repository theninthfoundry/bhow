"""Idempotent writes keyed to a single authenticated actor, dog and operation."""
import hashlib
import json
from collections.abc import Callable

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from bhow_api.models import IdempotencyRecord


def persist_once[T](
    db: Session,
    *,
    actor: str,
    dog_id: str,
    operation: str,
    key: str | None,
    payload: dict[str, object],
    create: Callable[[], T],
    lookup: Callable[[str], T | None],
) -> T:
    if key is None:
        obj = create()
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()
    scope = (IdempotencyRecord.actor == actor, IdempotencyRecord.dog_id == dog_id,
             IdempotencyRecord.operation == operation, IdempotencyRecord.request_key == key)

    def replay() -> T | None:
        prior = db.scalar(select(IdempotencyRecord).where(*scope))
        if prior is None:
            return None
        if prior.payload_digest != digest:
            raise HTTPException(status_code=409, detail="Idempotency key already used for different input")
        original = lookup(prior.result_id)
        if original is None:
            # Could happen after explicit deletion. Fail rather than duplicating.
            raise HTTPException(status_code=409, detail="Original record is no longer available")
        return original

    previous = replay()
    if previous is not None:
        return previous
    obj = create()
    db.add(obj)
    db.flush()
    db.add(IdempotencyRecord(actor=actor, dog_id=dog_id, operation=operation,
                             request_key=key, payload_digest=digest, result_id=obj.id))
    try:
        db.commit()
    except IntegrityError:
        # Another concurrent writer may have won the uniqueness race.
        db.rollback()
        previous = replay()
        if previous is not None:
            return previous
        raise
    db.refresh(obj)
    return obj
