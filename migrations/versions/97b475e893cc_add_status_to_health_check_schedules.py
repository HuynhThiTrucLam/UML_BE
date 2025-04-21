"""add_status_to_health_check_schedules

Revision ID: 97b475e893cc
Revises: ee43b61e18cd
Create Date: 2025-04-18 09:59:45.229204

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "97b475e893cc"
down_revision: Union[str, None] = "ee43b61e18cd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add the status column with default value 'scheduled'
    op.add_column(
        "health_check_schedules",
        sa.Column("status", sa.String(), nullable=False, server_default="scheduled"),
    )

    # Add the check constraint for valid status values
    op.create_check_constraint(
        "check_status_valid",
        "health_check_schedules",
        "status IN ('scheduled', 'in_progress', 'completed', 'canceled')",
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop the check constraint first
    op.drop_constraint("check_status_valid", "health_check_schedules", type_="check")

    # Then drop the status column
    op.drop_column("health_check_schedules", "status")
