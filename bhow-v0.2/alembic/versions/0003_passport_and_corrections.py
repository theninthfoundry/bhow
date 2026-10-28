"""Add dog passport fields and care event correction audit pointers.
Revision ID: 0003
Revises: 0002
"""
from collections.abc import Sequence
from alembic import op
import sqlalchemy as sa

revision: str = "0003"
down_revision: str | None = "0002"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    # 1. Extend dogs table with care passport fields
    op.add_column("dogs", sa.Column("allergies_reported", sa.Text(), nullable=True))
    op.add_column("dogs", sa.Column("conditions_reported", sa.Text(), nullable=True))
    op.add_column("dogs", sa.Column("medications_reported", sa.Text(), nullable=True))
    op.add_column("dogs", sa.Column("microchip_id", sa.String(length=64), nullable=True))
    op.add_column("dogs", sa.Column("veterinarian_contact", sa.Text(), nullable=True))

    # 2. Extend care_events table with correction pointers and audit reason
    op.add_column(
        "care_events",
        sa.Column("supersedes_event_id", sa.String(length=36), sa.ForeignKey("care_events.id", ondelete="SET NULL"), nullable=True),
    )
    op.add_column("care_events", sa.Column("correction_reason", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("care_events", "correction_reason")
    op.drop_column("care_events", "supersedes_event_id")
    op.drop_column("dogs", "veterinarian_contact")
    op.drop_column("dogs", "microchip_id")
    op.drop_column("dogs", "medications_reported")
    op.drop_column("dogs", "conditions_reported")
    op.drop_column("dogs", "allergies_reported")
