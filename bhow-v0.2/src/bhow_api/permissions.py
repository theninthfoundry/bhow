"""Object-level permission check: ownership cannot be bypassed by guessing dog IDs."""
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from bhow_api.models import Dog, DogCaregiver


def authorized_dog(session: Session, dog_id: str, subject: str) -> Dog:
    query = (
        select(Dog)
        .join(DogCaregiver, DogCaregiver.dog_id == Dog.id)
        .where(Dog.id == dog_id, DogCaregiver.subject == subject)
    )
    dog = session.scalar(query)
    if dog is None:
        # 404 to avoid disclosing whether another user's dog exists.
        raise HTTPException(status_code=404, detail="Dog not found")
    return dog
