"""UI-neutral data formatting. Tests don't require the Flet runtime."""
from datetime import date, datetime
from typing import Any


def friendly_date(value: str, today: date | None = None) -> str:
    due = date.fromisoformat(value[:10])
    day = today or date.today()
    if due == day:
        return "Today"
    if (due - day).days == 1:
        return "Tomorrow"
    if due < day:
        return f"Overdue · {due.strftime('%d %b')}"
    return due.strftime("%d %b %Y")


def historical_date(value: str) -> str:
    """A past observation is not an overdue care task."""
    return date.fromisoformat(value[:10]).strftime("%d %b %Y")


def next_action(overview: dict[str, Any]) -> tuple[str, str]:
    tasks = overview.get("pending_tasks", [])
    if tasks:
        next_one = tasks[0]
        return next_one["title"], friendly_date(next_one["due_on"])
    return "A care record starts with one small step.", "Add your first reminder"


def event_source(event: dict[str, Any]) -> str:
    # Server truth; a client must never silently upgrade records to verified.
    if event.get("verified") is True:
        return "Verified professional record"
    return "Caregiver entry · not vet verified"


def safe_ingredient_status(result: dict[str, Any]) -> tuple[str, str]:
    # The service never returns 'safe'. Fail closed even for unexpected responses.
    if result.get("status") == "potential_hazard":
        return "POTENTIAL HAZARD", "Some ingredients need attention."
    return "NOT ASSESSED AS SAFE", "No known match does not mean safe."


def short_date_now() -> str:
    return datetime.now().astimezone().date().isoformat()
