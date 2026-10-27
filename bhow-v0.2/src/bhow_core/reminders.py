"""Non-clinical due-date semantics; dates originate from the caregiver/vet."""
from datetime import date
from enum import StrEnum


class DueState(StrEnum):
    UPCOMING = "upcoming"
    DUE_TODAY = "due_today"
    OVERDUE = "overdue"
    COMPLETED = "completed"


def due_state(due: date, *, today: date, completed: bool) -> DueState:
    if completed:
        return DueState.COMPLETED
    if due < today:
        return DueState.OVERDUE
    if due == today:
        return DueState.DUE_TODAY
    return DueState.UPCOMING
