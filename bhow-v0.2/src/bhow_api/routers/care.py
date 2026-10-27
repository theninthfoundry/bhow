"""Care events are append-only and user-submitted entries are never marked verified."""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from bhow_api.db import get_db
from bhow_api.models import CareEvent, CareTask
from bhow_api.permissions import authorized_dog
from bhow_api.schemas import EventCreate, EventOut, TaskCreate, TaskOut
from bhow_api.security import Principal, current_principal

router = APIRouter(prefix="/dogs/{dog_id}", tags=["care"])
User = Annotated[Principal, Depends(current_principal)]
Db = Annotated[Session, Depends(get_db)]


@router.post("/events", response_model=EventOut, status_code=201)
def create_event(dog_id: UUID, payload: EventCreate, user: User, db: Db) -> CareEvent:
    authorized_dog(db, str(dog_id), user.subject)
    event = CareEvent(dog_id=str(dog_id), **payload.model_dump(), source="caregiver", verified=False, created_by=user.subject)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@router.get("/events", response_model=list[EventOut])
def list_events(dog_id: UUID, user: User, db: Db, limit: Annotated[int, Query(ge=1, le=100)] = 50) -> list[CareEvent]:
    authorized_dog(db, str(dog_id), user.subject)
    return list(db.scalars(select(CareEvent).where(CareEvent.dog_id == str(dog_id)).order_by(CareEvent.occurred_on.desc(), CareEvent.id).limit(limit)))


@router.post("/tasks", response_model=TaskOut, status_code=201)
def create_task(dog_id: UUID, payload: TaskCreate, user: User, db: Db) -> CareTask:
    authorized_dog(db, str(dog_id), user.subject)
    task = CareTask(dog_id=str(dog_id), **payload.model_dump(), scheduled_by=user.subject)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/tasks", response_model=list[TaskOut])
def list_tasks(dog_id: UUID, user: User, db: Db) -> list[CareTask]:
    authorized_dog(db, str(dog_id), user.subject)
    return list(db.scalars(select(CareTask).where(CareTask.dog_id == str(dog_id)).order_by(CareTask.due_on, CareTask.id).limit(100)))


@router.post("/tasks/{task_id}/complete", response_model=TaskOut)
def complete_task(dog_id: UUID, task_id: UUID, user: User, db: Db) -> CareTask:
    authorized_dog(db, str(dog_id), user.subject)
    task = db.scalar(select(CareTask).where(CareTask.id == str(task_id), CareTask.dog_id == str(dog_id)))
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = "completed"
    db.commit()
    db.refresh(task)
    return task
