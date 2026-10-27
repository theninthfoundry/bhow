"""Dog profile endpoints with authorization on EVERY object-level operation."""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from bhow_api.db import get_db
from bhow_api.models import Dog, DogCaregiver
from bhow_api.permissions import authorized_dog
from bhow_api.schemas import DogCreate, DogOut, DogPatch
from bhow_api.security import Principal, current_principal

router = APIRouter(prefix="/dogs", tags=["dogs"])
User = Annotated[Principal, Depends(current_principal)]
Db = Annotated[Session, Depends(get_db)]


@router.post("", response_model=DogOut, status_code=status.HTTP_201_CREATED)
def add_dog(payload: DogCreate, user: User, db: Db) -> Dog:
    dog = Dog(**payload.model_dump())
    db.add(dog)
    db.flush()
    db.add(DogCaregiver(dog_id=dog.id, subject=user.subject, role="owner"))
    db.commit()
    db.refresh(dog)
    return dog


@router.get("", response_model=list[DogOut])
def list_dogs(user: User, db: Db, limit: Annotated[int, Query(ge=1, le=100)] = 50) -> list[Dog]:
    stmt = (
        select(Dog)
        .join(DogCaregiver, DogCaregiver.dog_id == Dog.id)
        .where(DogCaregiver.subject == user.subject)
        .order_by(Dog.created_at.desc(), Dog.id)
        .limit(limit)
    )
    return list(db.scalars(stmt))


@router.get("/{dog_id}", response_model=DogOut)
def read_dog(dog_id: UUID, user: User, db: Db) -> Dog:
    return authorized_dog(db, str(dog_id), user.subject)


@router.patch("/{dog_id}", response_model=DogOut)
def patch_dog(dog_id: UUID, payload: DogPatch, user: User, db: Db) -> Dog:
    dog = authorized_dog(db, str(dog_id), user.subject)
    for field, value in payload.model_dump(exclude_unset=True).items():
        if field == "name" and value is None:
            raise HTTPException(status_code=422, detail="Name cannot be null")
        setattr(dog, field, value)
    db.commit()
    db.refresh(dog)
    return dog


@router.delete("/{dog_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_dog(dog_id: UUID, user: User, db: Db) -> None:
    dog = authorized_dog(db, str(dog_id), user.subject)
    # Single-owner deletion only: sharing will use explicit access revocation later.
    owners = [c for c in dog.caregivers if c.role == "owner"]
    if len(owners) != 1 or owners[0].subject != user.subject:
        raise HTTPException(status_code=409, detail="Cannot delete shared record")
    db.delete(dog)
    db.commit()
