"""add_timestamps_to_personal_infor_documents

Revision ID: b6373fc66fb2
Revises: 2d643721759c
Create Date: 2025-04-20 11:33:54.348566

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b6373fc66fb2"
down_revision: Union[str, None] = "2d643721759c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add created_at column with current timestamp as default
    op.add_column(
        "personal_infor_documents",
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("NOW()"), nullable=False
        ),
    )

    # Add updated_at column with current timestamp as default
    op.add_column(
        "personal_infor_documents",
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("NOW()"), nullable=False
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Remove the columns if downgrading
    op.drop_column("personal_infor_documents", "updated_at")
    op.drop_column("personal_infor_documents", "created_at")
