"""update_users_table_add_username_phone

Revision ID: ed267e68dea6
Revises: 9f787d5d645e
Create Date: 2025-04-16 14:13:59.114999

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ed267e68dea6"
down_revision: Union[str, None] = "9f787d5d645e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add user_name column with not null constraint and an index
    op.add_column(
        "users",
        sa.Column(
            "user_name", sa.String(), nullable=False, server_default="default_username"
        ),
    )
    op.create_index(op.f("ix_users_user_name"), "users", ["user_name"], unique=False)

    # Add phone_number column with not null constraint and an index
    op.add_column(
        "users",
        sa.Column(
            "phone_number", sa.String(), nullable=False, server_default="0000000000"
        ),
    )
    op.create_index(
        op.f("ix_users_phone_number"), "users", ["phone_number"], unique=False
    )

    # After migration is applied, remove the server_default values
    op.alter_column("users", "user_name", server_default=None)
    op.alter_column("users", "phone_number", server_default=None)


def downgrade() -> None:
    """Downgrade schema."""
    # Remove the indexes
    op.drop_index(op.f("ix_users_phone_number"), table_name="users")
    op.drop_index(op.f("ix_users_user_name"), table_name="users")

    # Remove the columns
    op.drop_column("users", "phone_number")
    op.drop_column("users", "user_name")
