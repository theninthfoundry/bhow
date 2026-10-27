"""External contracts, distinct from persistence and domain models."""
from datetime import date, datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class DogCreate(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    date_of_birth: date | None = None
    estimated_age_months: int | None = Field(default=None, ge=0, le=360)
    breed_reported: str | None = Field(default=None, max_length=120)
    weight_kg: float | None = Field(default=None, gt=0, le=150)
    care_context: Literal["owned", "foster", "community"] = "owned"

    @field_validator("name")
    @classmethod
    def clean_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Dog name cannot be blank")
        return value

    @model_validator(mode="after")
    def check_ages(self) -> "DogCreate":
        if self.date_of_birth and self.estimated_age_months is not None:
            raise ValueError("Supply birth date OR estimated age, not both")
        if self.date_of_birth and self.date_of_birth > date.today():
            raise ValueError("Birth date cannot be in the future")
        return self


class DogPatch(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=80)

    @field_validator("name")
    @classmethod
    def clean_name(cls, value: str | None) -> str | None:
        if value is None:
            raise ValueError("Dog name cannot be null")
        value = value.strip()
        if not value:
            raise ValueError("Dog name cannot be blank")
        return value
    breed_reported: str | None = Field(default=None, max_length=120)
    weight_kg: float | None = Field(default=None, gt=0, le=150)


class DogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    date_of_birth: date | None
    estimated_age_months: int | None
    breed_reported: str | None
    weight_kg: float | None
    care_context: str
    created_at: datetime


class EventCreate(BaseModel):
    kind: Literal["weight", "vaccination", "visit", "symptom", "nutrition", "milestone", "other"]
    notes: str = Field(min_length=1, max_length=3000)
    occurred_on: date


class EventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    kind: str
    notes: str
    occurred_on: date
    source: str
    verified: bool
    recorded_at: datetime


class TaskCreate(BaseModel):
    kind: Literal["vaccination", "appointment", "parasite_prevention", "grooming", "other"]
    title: str = Field(min_length=1, max_length=140)
    due_on: date


class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    title: str
    kind: str
    due_on: date
    status: str


class FoodCheckIn(BaseModel):
    ingredients_text: str = Field(min_length=1, max_length=3000)
    already_eaten: bool = False


class FoodFlag(BaseModel):
    ingredient: str
    reference: str
    source_url: str
    reviewed_by_vet: bool


class FoodCheckOut(BaseModel):
    status: Literal["potential_hazard", "unknown"]
    flagged: list[FoodFlag]
    summary: str
    next_step: str
    kb_release_status: str = "educational_preview_not_vet_reviewed"


class PrincipalOut(BaseModel):
    subject: str


class DogOverview(BaseModel):
    """Activity and task snapshot; not a dog wellbeing score."""
    dog: DogOut
    pending_count: int = Field(ge=0)
    overdue_count: int = Field(ge=0)
    pending_tasks: list[TaskOut]
    recent_events: list[EventOut]
    generated_on: date
    status: Literal["records_only_no_clinical_assessment"]


class CursorPage[T](BaseModel):
    items: list[T]
    next_cursor: str | None = None
