"""User export and deletion for initial single-owner records (document uploads not yet built)."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from bhow_api.db import get_db
from bhow_api.models import Dog, DogCaregiver, IdempotencyRecord
from bhow_api.schemas import DogOut, EventOut, PrincipalOut, TaskOut
from bhow_api.security import Principal, current_principal

router = APIRouter(prefix="/account", tags=["account"])
User = Annotated[Principal, Depends(current_principal)]
Db = Annotated[Session, Depends(get_db)]


@router.get("/me", response_model=PrincipalOut)
def me(user: User) -> PrincipalOut:
    return PrincipalOut(subject=user.subject)


@router.get("/export")
def export_data(user: User, db: Db) -> dict[str, object]:
    dogs = list(db.scalars(select(Dog).join(DogCaregiver).where(DogCaregiver.subject == user.subject)))
    return {
        "subject": user.subject,
        "dogs": [
            {
                **DogOut.model_validate(dog).model_dump(mode="json"),
                "events": [EventOut.model_validate(e).model_dump(mode="json") for e in dog.events],
                "tasks": [TaskOut.model_validate(t).model_dump(mode="json") for t in dog.tasks],
            }
            for dog in dogs
        ],
        "notice": "Export includes MVP database records only; future integrations require separate coverage.",
    }


@router.delete("/me", status_code=204)
def delete_account_data(user: User, db: Db) -> None:
    memberships = list(db.scalars(select(DogCaregiver).where(DogCaregiver.subject == user.subject)))
    for membership in memberships:
        dog = db.get(Dog, membership.dog_id)
        if dog is None:
            continue
        if any(c.subject != user.subject for c in dog.caregivers):
            raise HTTPException(status_code=409, detail="Shared dog records require a transfer or access revocation first")
        db.execute(delete(IdempotencyRecord).where(IdempotencyRecord.dog_id == dog.id))
        db.delete(dog)
    db.commit()
    # IMPORTANT: identity provider account deletion must happen there separately.
