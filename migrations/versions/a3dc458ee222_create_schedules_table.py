"""create_schedules_table

Revision ID: a3dc458ee222
Revises: ed267e68dea6
Create Date: 2025-04-16 17:28:07.904946

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import uuid


# revision identifiers, used by Alembic.
revision: str = "a3dc458ee222"
down_revision: Union[str, None] = "ed267e68dea6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "schedules",
        sa.Column("id", sa.UUID(), nullable=False, default=uuid.uuid4),
        sa.Column("course_id", sa.UUID(), nullable=False),
        sa.Column("schedule_datetime", sa.String(), nullable=False),
        sa.Column("start_time", sa.String(), nullable=False),
        sa.Column("end_time", sa.String(), nullable=False),
        sa.Column("location", sa.String(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("instructor_id", sa.UUID(), nullable=False),
        sa.Column("vehicle_id", sa.UUID(), nullable=False),
        sa.Column("max_students", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_schedules_id"), "schedules", ["id"], unique=False)
    op.create_index(
        op.f("ix_schedules_course_id"), "schedules", ["course_id"], unique=False
    )
    op.create_index(
        op.f("ix_schedules_schedule_datetime"),
        "schedules",
        ["schedule_datetime"],
        unique=False,
    )
    op.create_index(
        op.f("ix_schedules_start_time"), "schedules", ["start_time"], unique=False
    )
    op.create_index(
        op.f("ix_schedules_end_time"), "schedules", ["end_time"], unique=False
    )
    op.create_index(
        op.f("ix_schedules_location"), "schedules", ["location"], unique=False
    )
    op.create_index(op.f("ix_schedules_type"), "schedules", ["type"], unique=False)
    op.create_index(
        op.f("ix_schedules_instructor_id"), "schedules", ["instructor_id"], unique=False
    )
    op.create_index(
        op.f("ix_schedules_vehicle_id"), "schedules", ["vehicle_id"], unique=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_schedules_vehicle_id"), table_name="schedules")
    op.drop_index(op.f("ix_schedules_instructor_id"), table_name="schedules")
    op.drop_index(op.f("ix_schedules_type"), table_name="schedules")
    op.drop_index(op.f("ix_schedules_location"), table_name="schedules")
    op.drop_index(op.f("ix_schedules_end_time"), table_name="schedules")
    op.drop_index(op.f("ix_schedules_start_time"), table_name="schedules")
    op.drop_index(op.f("ix_schedules_schedule_datetime"), table_name="schedules")
    op.drop_index(op.f("ix_schedules_course_id"), table_name="schedules")
    op.drop_index(op.f("ix_schedules_id"), table_name="schedules")
    op.drop_table("schedules")
