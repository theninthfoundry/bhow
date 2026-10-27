"""Read-only member-scoped overview; task dates are not clinical schedules."""
from datetime import datetime
from typing import Annotated
from uuid import UUID
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from bhow_api.db import get_db
from bhow_api.models import CareEvent, CareTask
from bhow_api.permissions import authorized_dog
from bhow_api.schemas import DogOverview
from bhow_api.security import Principal, current_principal

router = APIRouter(prefix="/dogs/{dog_id}", tags=["today"])
User = Annotated[Principal, Depends(current_principal)]
Db = Annotated[Session, Depends(get_db)]


@router.get("/overview", response_model=DogOverview)
def dog_overview(
    dog_id: UUID,
    user: User,
    db: Db,
    tz: Annotated[str, Query(max_length=64, description="IANA time zone for due dates")] = "Asia/Kolkata",
) -> DogOverview:
    dog = authorized_dog(db, str(dog_id), user.subject)
    try:
        today = datetime.now(ZoneInfo(tz)).date()
    except (ZoneInfoNotFoundError, ValueError) as exc:
        raise HTTPException(status_code=422, detail="Provide a valid IANA time zone") from exc
    pending = db.scalar(
        select(func.count(CareTask.id)).where(
            CareTask.dog_id == dog.id, CareTask.status == "pending"
        )
    ) or 0
    overdue = db.scalar(
        select(func.count(CareTask.id)).where(
            CareTask.dog_id == dog.id,
            CareTask.status == "pending",
            CareTask.due_on < today,
        )
    ) or 0
    tasks = list(
        db.scalars(
            select(CareTask)
            .where(CareTask.dog_id == dog.id, CareTask.status == "pending")
            .order_by(CareTask.due_on, CareTask.id)
            .limit(5)
        )
    )
    events = list(
        db.scalars(
            select(CareEvent)
            .where(CareEvent.dog_id == dog.id)
            .order_by(CareEvent.occurred_on.desc(), CareEvent.recorded_at.desc(), CareEvent.id)
            .limit(5)
        )
    )
    return DogOverview(
        dog=dog,
        pending_count=pending,
        overdue_count=overdue,
        pending_tasks=tasks,
        recent_events=events,
        generated_on=today,
        status="records_only_no_clinical_assessment",
    )
