"""create_instructors_table

Revision ID: ee43b61e18cd
Revises: a3dc458ee222
Create Date: 2025-04-16 17:31:43.755668

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import uuid


# revision identifiers, used by Alembic.
revision: str = 'ee43b61e18cd'
down_revision: Union[str, None] = 'a3dc458ee222'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('instructors',
        sa.Column('id', sa.UUID(), nullable=False, default=uuid.uuid4),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('certification', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='instructors_user_id_fkey')
    )
    op.create_index(op.f('ix_instructors_id'), 'instructors', ['id'], unique=False)
    op.create_index(op.f('ix_instructors_user_id'), 'instructors', ['user_id'], unique=False)
    op.create_index(op.f('ix_instructors_certification'), 'instructors', ['certification'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_instructors_certification'), table_name='instructors')
    op.drop_index(op.f('ix_instructors_user_id'), table_name='instructors')
    op.drop_index(op.f('ix_instructors_id'), table_name='instructors')
    op.drop_table('instructors')
