"""fix_payment_vehicle_relationships

Revision ID: 3205b0c2b431
Revises: 14c350b7c896
Create Date: 2025-04-21 08:01:31.139088

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "3205b0c2b431"
down_revision: Union[str, None] = "14c350b7c896"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Fix payment_method_id in payments table (change from UUID to Integer)
    op.alter_column(
        "payments",
        "payment_method_id",
        existing_type=postgresql.UUID(),
        type_=sa.Integer(),
        existing_nullable=True,
    )

    # 2. Fix course_registration_id in payments to point to course_registrations.id instead of courses.id
    op.drop_constraint(
        "payments_course_registration_id_fkey", "payments", type_="foreignkey"
    )
    op.create_foreign_key(
        "payments_course_registration_id_fkey",
        "payments",
        "course_registrations",
        ["course_registration_id"],
        ["id"],
    )

    # 3. Add vehicle relationship to schedules
    op.create_foreign_key(
        "schedules_vehicle_id_fkey", "schedules", "vehicles", ["vehicle_id"], ["id"]
    )

    # 4. Create relationship between course_registrations and schedules
    if not op.get_bind().dialect.has_table(
        op.get_bind(), "course_registration_schedule"
    ):
        op.create_table(
            "course_registration_schedule",
            sa.Column("course_registration_id", postgresql.UUID(), nullable=False),
            sa.Column("schedule_id", postgresql.UUID(), nullable=False),
            sa.ForeignKeyConstraint(
                ["course_registration_id"],
                ["course_registrations.id"],
            ),
            sa.ForeignKeyConstraint(
                ["schedule_id"],
                ["schedules.id"],
            ),
            sa.PrimaryKeyConstraint("course_registration_id", "schedule_id"),
        )


def downgrade() -> None:
    """Downgrade schema."""
    # 4. Remove relationship between course_registrations and schedules
    op.drop_table("course_registration_schedule")

    # 3. Remove vehicle relationship from schedules
    op.drop_constraint("schedules_vehicle_id_fkey", "schedules", type_="foreignkey")

    # 2. Revert course_registration_id in payments to point back to courses.id
    op.drop_constraint(
        "payments_course_registration_id_fkey", "payments", type_="foreignkey"
    )
    op.create_foreign_key(
        "payments_course_registration_id_fkey",
        "payments",
        "courses",
        ["course_registration_id"],
        ["id"],
    )

    # 1. Revert payment_method_id in payments table back to UUID
    op.alter_column(
        "payments",
        "payment_method_id",
        existing_type=sa.Integer(),
        type_=postgresql.UUID(),
        existing_nullable=True,
    )
