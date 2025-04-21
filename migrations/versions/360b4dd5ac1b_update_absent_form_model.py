"""update_absent_form_model

Revision ID: 360b4dd5ac1b
Revises: 991d9ae13101
Create Date: 2025-04-21 16:50:54.137537

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid


# revision identifiers, used by Alembic.
revision: str = '360b4dd5ac1b'
down_revision: Union[str, None] = '991d9ae13101'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Check if table exists
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    if "absent_forms" in inspector.get_table_names():
        # Table exists, alter it
        op.alter_column('absent_forms', 'id',
                       existing_type=sa.UUID(),
                       nullable=False,
                       server_default=sa.text('uuid_generate_v4()'))
        
        # Add index on id column if it doesn't exist
        op.create_index(op.f('ix_absent_forms_id'), 'absent_forms', ['id'], unique=False)
        
    else:
        # Table doesn't exist, create it
        op.create_table('absent_forms',
            sa.Column('id', sa.UUID(), nullable=False, server_default=sa.text('uuid_generate_v4()')),
            sa.Column('object_id', sa.UUID(), nullable=True),
            sa.Column('type', sa.String(), nullable=True),
            sa.Column('phone_number', sa.String(), nullable=True),
            sa.Column('reason', sa.String(), nullable=True), 
            sa.Column('evidence', sa.String(), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_absent_forms_id'), 'absent_forms', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # We don't drop the table in downgrade since it might contain important data
    # Instead, we revert specific changes
    
    op.alter_column('absent_forms', 'id',
                   existing_type=sa.UUID(),
                   nullable=False,
                   server_default=None)
