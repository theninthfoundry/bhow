"""Initial care records schema.

Revision ID: 0001
Revises:
"""
from collections.abc import Sequence
from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision: str | None = None
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "dogs",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(80), nullable=False),
        sa.Column("date_of_birth", sa.Date(), nullable=True),
        sa.Column("estimated_age_months", sa.Integer(), nullable=True),
        sa.Column("breed_reported", sa.String(120), nullable=True),
        sa.Column("weight_kg", sa.Numeric(6, 2, asdecimal=False), nullable=True),
        sa.Column("care_context", sa.String(24), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "dog_caregivers",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("dog_id", sa.String(36), sa.ForeignKey("dogs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("subject", sa.String(255), nullable=False),
        sa.Column("role", sa.String(16), nullable=False),
        sa.UniqueConstraint("dog_id", "subject", name="uq_dog_subject"),
    )
    op.create_index("ix_caregiver_subject", "dog_caregivers", ["subject"])
    op.create_table(
        "care_events",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("dog_id", sa.String(36), sa.ForeignKey("dogs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("kind", sa.String(32), nullable=False),
        sa.Column("notes", sa.Text(), nullable=False),
        sa.Column("occurred_on", sa.Date(), nullable=False),
        sa.Column("source", sa.String(24), nullable=False),
        sa.Column("verified", sa.Boolean(), nullable=False),
        sa.Column("created_by", sa.String(255), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_event_dog_date", "care_events", ["dog_id", "occurred_on"])
    op.create_table(
        "care_tasks",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("dog_id", sa.String(36), sa.ForeignKey("dogs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(140), nullable=False),
        sa.Column("kind", sa.String(32), nullable=False),
        sa.Column("due_on", sa.Date(), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("scheduled_by", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_task_dog_due", "care_tasks", ["dog_id", "due_on"])


def downgrade() -> None:
    op.drop_index("ix_task_dog_due", table_name="care_tasks")
    op.drop_table("care_tasks")
    op.drop_index("ix_event_dog_date", table_name="care_events")
    op.drop_table("care_events")
    op.drop_index("ix_caregiver_subject", table_name="dog_caregivers")
    op.drop_table("dog_caregivers")
    op.drop_table("dogs")

# Migration downgrade safety checks added
