"""add_updated_at_to_health_check_documents

Revision ID: 2d643721759c
Revises: 9e2c9a6f6c2f
Create Date: 2025-04-18 12:16:45.612581

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = '2d643721759c'
down_revision: Union[str, None] = '9e2c9a6f6c2f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add updated_at column to health_check_documents table."""
    op.add_column('health_check_documents', 
                  sa.Column('updated_at', sa.DateTime(), 
                           nullable=False, 
                           server_default=sa.text('now()')))


def downgrade() -> None:
    """Remove updated_at column from health_check_documents table."""
    op.drop_column('health_check_documents', 'updated_at')
