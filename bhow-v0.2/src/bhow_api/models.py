"""Persistence representations. NEVER infer verification from a user's claim."""
from datetime import UTC, date, datetime
from uuid import uuid4

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Index, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bhow_api.db import Base


def uid() -> str:
    return str(uuid4())


def utcnow() -> datetime:
    return datetime.now(UTC)


class Dog(Base):
    __tablename__ = "dogs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    date_of_birth: Mapped[date | None] = mapped_column(Date, nullable=True)
    estimated_age_months: Mapped[int | None] = mapped_column(nullable=True)
    breed_reported: Mapped[str | None] = mapped_column(String(120), nullable=True)
    weight_kg: Mapped[float | None] = mapped_column(Numeric(6, 2, asdecimal=False), nullable=True)
    care_context: Mapped[str] = mapped_column(String(24), default="owned", nullable=False)
    allergies_reported: Mapped[str | None] = mapped_column(Text, nullable=True)
    conditions_reported: Mapped[str | None] = mapped_column(Text, nullable=True)
    medications_reported: Mapped[str | None] = mapped_column(Text, nullable=True)
    microchip_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    veterinarian_contact: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    caregivers: Mapped[list["DogCaregiver"]] = relationship(cascade="all, delete-orphan", back_populates="dog")
    events: Mapped[list["CareEvent"]] = relationship(cascade="all, delete-orphan", back_populates="dog")
    tasks: Mapped[list["CareTask"]] = relationship(cascade="all, delete-orphan", back_populates="dog")


class DogCaregiver(Base):
    __tablename__ = "dog_caregivers"
    __table_args__ = (UniqueConstraint("dog_id", "subject", name="uq_dog_subject"), Index("ix_caregiver_subject", "subject"))

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    dog_id: Mapped[str] = mapped_column(ForeignKey("dogs.id", ondelete="CASCADE"), nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(16), default="owner")
    dog: Mapped[Dog] = relationship(back_populates="caregivers")


class CareEvent(Base):
    __tablename__ = "care_events"
    __table_args__ = (Index("ix_event_dog_date", "dog_id", "occurred_on"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    dog_id: Mapped[str] = mapped_column(ForeignKey("dogs.id", ondelete="CASCADE"), nullable=False)
    kind: Mapped[str] = mapped_column(String(32), nullable=False)
    notes: Mapped[str] = mapped_column(Text, nullable=False)
    occurred_on: Mapped[date] = mapped_column(Date, nullable=False)
    source: Mapped[str] = mapped_column(String(24), default="caregiver", nullable=False)
    verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_by: Mapped[str] = mapped_column(String(255), nullable=False)
    supersedes_event_id: Mapped[str | None] = mapped_column(ForeignKey("care_events.id", ondelete="SET NULL"), nullable=True)
    correction_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    dog: Mapped[Dog] = relationship(back_populates="events", foreign_keys=[dog_id])


class CareTask(Base):
    __tablename__ = "care_tasks"
    __table_args__ = (Index("ix_task_dog_due", "dog_id", "due_on"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    dog_id: Mapped[str] = mapped_column(ForeignKey("dogs.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(140), nullable=False)
    kind: Mapped[str] = mapped_column(String(32), nullable=False)
    due_on: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    scheduled_by: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    dog: Mapped[Dog] = relationship(back_populates="tasks")


class IdempotencyRecord(Base):
    """A committed response pointer. Unique DB constraint serializes concurrent retries."""
    __tablename__ = "idempotency_records"
    __table_args__ = (UniqueConstraint("actor", "dog_id", "operation", "request_key", name="uq_idempotency_scope"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uid)
    actor: Mapped[str] = mapped_column(String(255), nullable=False)
    dog_id: Mapped[str] = mapped_column(String(36), nullable=False)
    operation: Mapped[str] = mapped_column(String(30), nullable=False)
    request_key: Mapped[str] = mapped_column(String(128), nullable=False)
    payload_digest: Mapped[str] = mapped_column(String(64), nullable=False)
    result_id: Mapped[str] = mapped_column(String(36), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
