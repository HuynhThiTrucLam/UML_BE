"""allow_null_in_health_check_document

Revision ID: 9e2c9a6f6c2f
Revises: 9d702150479b
Create Date: 2025-04-18 12:00:02.185626

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9e2c9a6f6c2f"
down_revision: Union[str, None] = "9d702150479b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema to allow NULL in document field."""
    op.alter_column(
        "health_check_documents", "document", existing_type=sa.String(), nullable=True
    )


def downgrade() -> None:
    """Downgrade schema back to NOT NULL for document field."""
    op.alter_column(
        "health_check_documents", "document", existing_type=sa.String(), nullable=False
    )
