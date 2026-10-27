"""Retry-safe care writes.
Revision ID: 0002
Revises: 0001
"""
from collections.abc import Sequence
from alembic import op
import sqlalchemy as sa

revision: str = "0002"
down_revision: str | None = "0001"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "idempotency_records",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("actor", sa.String(255), nullable=False),
        sa.Column("dog_id", sa.String(36), nullable=False),
        sa.Column("operation", sa.String(30), nullable=False),
        sa.Column("request_key", sa.String(128), nullable=False),
        sa.Column("payload_digest", sa.String(64), nullable=False),
        sa.Column("result_id", sa.String(36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("actor", "dog_id", "operation", "request_key", name="uq_idempotency_scope"),
    )


def downgrade() -> None:
    op.drop_table("idempotency_records")
