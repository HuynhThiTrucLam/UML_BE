"""create_personal_infor_documents

Revision ID: 30a6a777c348
Revises:
Create Date: 2025-04-16 10:23:50.738899

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import uuid


# revision identifiers, used by Alembic.
revision: str = "30a6a777c348"
down_revision: Union[str, None] = None  # This is the base migration
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create personal_infor_documents table
    op.create_table(
        "personal_infor_documents",
        sa.Column("id", sa.UUID(), nullable=False, default=uuid.uuid4),
        sa.Column("user_id", sa.UUID(), nullable=True),
        sa.Column("full_name", sa.String(), nullable=True),
        sa.Column("date_of_birth", sa.String(), nullable=True),
        sa.Column("gender", sa.String(), nullable=True),
        sa.Column("address", sa.String(), nullable=True),
        sa.Column("identity_number", sa.String(), nullable=True),
        sa.Column("identity_img_front", sa.String(), nullable=True),
        sa.Column("identity_img_back", sa.String(), nullable=True),
        sa.Column("avatar", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_personal_infor_documents_id"),
        "personal_infor_documents",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop personal_infor_documents table
    op.drop_index(
        op.f("ix_personal_infor_documents_id"), table_name="personal_infor_documents"
    )
    op.drop_table("personal_infor_documents")
