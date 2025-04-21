"""update_health_check_document_status

Revision ID: 53adc465e861
Revises: 4f0e53e39c0f
Create Date: 2025-04-16 12:08:41.740050

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision: str = "53adc465e861"
down_revision: Union[str, None] = "4f0e53e39c0f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop the existing check constraint
    op.drop_constraint(
        "check_valid_document_status", "health_check_documents", type_="check"
    )

    # Update any existing 'pending' status records to 'registered'
    conn = op.get_bind()
    conn.execute(
        text(
            "UPDATE health_check_documents SET status = 'registered' WHERE status = 'pending'"
        )
    )

    # Change the default value for the status column
    op.alter_column(
        "health_check_documents",
        "status",
        server_default="registered",
        existing_nullable=False,
    )

    # Add the constraint back with updated values that include 'registered' and 'checked'
    op.create_check_constraint(
        "check_valid_document_status",
        "health_check_documents",
        "status IN ('registered', 'checked')",
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop the updated constraint
    op.drop_constraint(
        "check_valid_document_status", "health_check_documents", type_="check"
    )

    # Change the default value back to 'pending'
    op.alter_column(
        "health_check_documents",
        "status",
        server_default="pending",
        existing_nullable=False,
    )

    # Add the original constraint back
    op.create_check_constraint(
        "check_valid_document_status",
        "health_check_documents",
        "status IN ('registered', 'checked')",
    )
