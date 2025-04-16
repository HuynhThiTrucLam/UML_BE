"""add license_type_id to courses table

Revision ID: a3092b36da52
Revises: e8d660349145
Create Date: 2025-04-16 13:53:13.141730

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a3092b36da52'
down_revision: Union[str, None] = 'e8d660349145'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add license_type_id column to courses table
    op.add_column('courses', sa.Column('license_type_id', postgresql.UUID(), nullable=True))
    op.create_index(op.f('ix_courses_license_type_id'), 'courses', ['license_type_id'], unique=False)
    op.create_foreign_key(None, 'courses', 'license_types', ['license_type_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    """Downgrade schema."""
    # Remove license_type_id column from courses table
    op.drop_constraint(None, 'courses', type_='foreignkey')
    op.drop_index(op.f('ix_courses_license_type_id'), table_name='courses')
    op.drop_column('courses', 'license_type_id')
