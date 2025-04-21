"""update_health_check_document_status

Revision ID: e2e14b87215a
Revises: 9ca27d9e8f3c
Create Date: 2025-04-16 11:23:00.208831

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = "e2e14b87215a"
down_revision: Union[str, None] = "9ca27d9e8f3c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create the uuid-ossp extension if it doesn't exist
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    # Check if the table exists
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    if "health_check_documents" not in inspector.get_table_names():
        # Create the table with the correct constraint and matching data types
        op.create_table(
            "health_check_documents",
            sa.Column(
                "id",
                postgresql.UUID(),
                nullable=False,
                server_default=sa.text("uuid_generate_v4()"),
            ),
            sa.Column("student_id", sa.Integer(), nullable=False),
            sa.Column(
                "health_check_id", sa.Integer(), nullable=False
            ),  # Changed to Integer to match db schema
            sa.Column("document", sa.String(), nullable=False),
            sa.Column("status", sa.String(), nullable=False, server_default="pending"),
            sa.Column(
                "created_at",
                sa.DateTime(),
                nullable=False,
                server_default=sa.text("CURRENT_TIMESTAMP"),
            ),
            sa.ForeignKeyConstraint(
                ["student_id"], ["students.id"], ondelete="CASCADE"
            ),
            sa.ForeignKeyConstraint(
                ["health_check_id"], ["health_check_schedules.id"], ondelete="CASCADE"
            ),
            sa.PrimaryKeyConstraint("id"),
            sa.CheckConstraint(
                "status IN ('registered', 'checked', 'pending')",
                name="check_valid_document_status",
            ),
        )
        op.create_index(
            op.f("ix_health_check_documents_id"),
            "health_check_documents",
            ["id"],
            unique=False,
        )
        op.create_index(
            op.f("ix_health_check_documents_student_id"),
            "health_check_documents",
            ["student_id"],
            unique=False,
        )
        op.create_index(
            op.f("ix_health_check_documents_health_check_id"),
            "health_check_documents",
            ["health_check_id"],
            unique=False,
        )
    else:
        # If the table exists, update the constraint
        try:
            op.drop_constraint(
                "check_valid_document_status", "health_check_documents", type_="check"
            )
        except:
            # Constraint may not exist, that's fine
            pass

        op.create_check_constraint(
            "check_valid_document_status",
            "health_check_documents",
            "status IN ('registered', 'checked', 'pending')",
        )


def downgrade() -> None:
    """Downgrade schema."""
    # Check if the table exists
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    if "health_check_documents" in inspector.get_table_names():
        try:
            op.drop_constraint(
                "check_valid_document_status", "health_check_documents", type_="check"
            )
            op.create_check_constraint(
                "check_valid_document_status",
                "health_check_documents",
                "status IN ('registered', 'checked')",
            )
        except:
            # Table might have been created by this migration, so we'll drop it completely
            op.drop_table("health_check_documents")
