"""update course_registrations schema (UUID id, new columns)

Revision ID: 7fad0257fa5d
Revises: 7818ddf4930a
Create Date: 2025-04-16 13:39:22.343885

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7fad0257fa5d'
down_revision: Union[str, None] = '7818ddf4930a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column('course_registrations', 'id')
    op.add_column('course_registrations', sa.Column('id', sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, nullable=False, server_default=sa.text('gen_random_uuid()')))
    op.add_column('course_registrations', sa.Column('created_at', sa.String(), nullable=False))
    op.add_column('course_registrations', sa.Column('updated_at', sa.String(), nullable=False))
    op.add_column('course_registrations', sa.Column('method', sa.String(), nullable=False))
    op.add_column('course_registrations', sa.Column('status', sa.String(), nullable=False, server_default='pending'))
    op.add_column('course_registrations', sa.Column('approved_at', sa.String()))
    op.add_column('course_registrations', sa.Column('rejected_at', sa.String()))
    op.add_column('course_registrations', sa.Column('note', sa.String()))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('course_registrations', 'note')
    op.drop_column('course_registrations', 'rejected_at')
    op.drop_column('course_registrations', 'approved_at')
    op.drop_column('course_registrations', 'status')
    op.drop_column('course_registrations', 'method')
    op.drop_column('course_registrations', 'updated_at')
    op.drop_column('course_registrations', 'created_at')
    op.drop_column('course_registrations', 'id')
    op.add_column('course_registrations', sa.Column('id', sa.String(), nullable=False))
