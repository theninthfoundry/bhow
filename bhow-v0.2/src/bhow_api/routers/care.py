"""Care records are append-only, caregiver-sourced, and retrievable across all pages."""
from datetime import date
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session

from bhow_api.db import get_db
from bhow_api.idempotency import persist_once
from bhow_api.models import CareEvent, CareTask
from bhow_api.pagination import decode_cursor, encode_cursor
from bhow_api.permissions import authorized_dog
from bhow_api.schemas import CursorPage, EventCreate, EventOut, TaskCreate, TaskOut
from bhow_api.security import Principal, current_principal

router = APIRouter(prefix="/dogs/{dog_id}", tags=["care"])
User = Annotated[Principal, Depends(current_principal)]
Db = Annotated[Session, Depends(get_db)]
Key = Annotated[str | None, Header(alias="Idempotency-Key", min_length=8, max_length=128)]
Limit = Annotated[int, Query(ge=1, le=100)]


@router.post("/events", response_model=EventOut, status_code=201)
def create_event(dog_id: UUID, payload: EventCreate, user: User, db: Db, idempotency_key: Key = None) -> CareEvent:
    authorized_dog(db, str(dog_id), user.subject)
    return persist_once(
        db, actor=user.subject, dog_id=str(dog_id), operation="create_event", key=idempotency_key,
        payload=payload.model_dump(mode="json"),
        create=lambda: CareEvent(dog_id=str(dog_id), **payload.model_dump(), source="caregiver",
                                 verified=False, created_by=user.subject),
        lookup=lambda rid: db.get(CareEvent, rid),
    )


@router.get("/events", response_model=list[EventOut], deprecated=True)
def list_events(dog_id: UUID, user: User, db: Db, limit: Limit = 50) -> list[CareEvent]:
    """Legacy first-page result; use /events/page for complete history."""
    authorized_dog(db, str(dog_id), user.subject)
    return list(db.scalars(select(CareEvent).where(CareEvent.dog_id == str(dog_id))
                           .order_by(CareEvent.occurred_on.desc(), CareEvent.id.desc()).limit(limit)))


@router.get("/events/page", response_model=CursorPage[EventOut])
def page_events(dog_id: UUID, user: User, db: Db, limit: Limit = 50,
                cursor: Annotated[str | None, Query(max_length=256)] = None) -> CursorPage[EventOut]:
    authorized_dog(db, str(dog_id), user.subject)
    query = select(CareEvent).where(CareEvent.dog_id == str(dog_id))
    if cursor:
        day, last_id = decode_cursor(cursor, (date, UUID))
        query = query.where(or_(CareEvent.occurred_on < day,
                                and_(CareEvent.occurred_on == day, CareEvent.id < last_id)))
    rows = list(db.scalars(query.order_by(CareEvent.occurred_on.desc(), CareEvent.id.desc()).limit(limit + 1)))
    more = len(rows) > limit
    items = rows[:limit]
    return CursorPage[EventOut](items=[EventOut.model_validate(x) for x in items],
                                next_cursor=encode_cursor(items[-1].occurred_on, items[-1].id) if more else None)


@router.post("/tasks", response_model=TaskOut, status_code=201)
def create_task(dog_id: UUID, payload: TaskCreate, user: User, db: Db, idempotency_key: Key = None) -> CareTask:
    authorized_dog(db, str(dog_id), user.subject)
    return persist_once(
        db, actor=user.subject, dog_id=str(dog_id), operation="create_task", key=idempotency_key,
        payload=payload.model_dump(mode="json"),
        create=lambda: CareTask(dog_id=str(dog_id), **payload.model_dump(), scheduled_by=user.subject),
        lookup=lambda rid: db.get(CareTask, rid),
    )


@router.get("/tasks", response_model=list[TaskOut], deprecated=True)
def list_tasks(dog_id: UUID, user: User, db: Db) -> list[CareTask]:
    authorized_dog(db, str(dog_id), user.subject)
    return list(db.scalars(select(CareTask).where(CareTask.dog_id == str(dog_id))
                           .order_by(CareTask.due_on, CareTask.id).limit(100)))


@router.get("/tasks/page", response_model=CursorPage[TaskOut])
def page_tasks(dog_id: UUID, user: User, db: Db, limit: Limit = 50,
               status_filter: Annotated[Literal["pending", "completed", "all"], Query(alias="status")] = "all",
               cursor: Annotated[str | None, Query(max_length=256)] = None) -> CursorPage[TaskOut]:
    authorized_dog(db, str(dog_id), user.subject)
    query = select(CareTask).where(CareTask.dog_id == str(dog_id))
    if status_filter != "all":
        query = query.where(CareTask.status == status_filter)
    if cursor:
        day, last_id = decode_cursor(cursor, (date, UUID))
        query = query.where(or_(CareTask.due_on > day,
                                and_(CareTask.due_on == day, CareTask.id > last_id)))
    rows = list(db.scalars(query.order_by(CareTask.due_on, CareTask.id).limit(limit + 1)))
    more = len(rows) > limit
    items = rows[:limit]
    return CursorPage[TaskOut](items=[TaskOut.model_validate(x) for x in items],
                               next_cursor=encode_cursor(items[-1].due_on, items[-1].id) if more else None)


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
