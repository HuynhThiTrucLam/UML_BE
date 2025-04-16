"""refactor_students_table_schema

Revision ID: 9f787d5d645e
Revises: bb6d40797222
Create Date: 2025-04-16 14:02:08.767266

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '9f787d5d645e'
down_revision: Union[str, None] = 'bb6d40797222'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Focused changes to students table
    op.drop_column('students', 'enrollment_number')
    op.drop_column('students', 'course_of_study')
    
    # Ensure proper indexing and constraints for user_id
    op.drop_index('ix_students_user_id', table_name='students', if_exists=True)
    op.create_unique_constraint('uq_students_user_id', 'students', ['user_id'])
    
    # Ensure id is UUID type
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = {c['name']: c for c in inspector.get_columns('students')}
    
    if not isinstance(columns.get('id', {}).get('type'), postgresql.UUID):
        # Add temporary UUID column
        op.add_column('students', sa.Column('id_new', postgresql.UUID(), nullable=True))
        
        # Generate UUIDs for all existing records
        op.execute("UPDATE students SET id_new = uuid_generate_v4()")
        
        # Drop the primary key
        op.drop_constraint('students_pkey', 'students', type_='primary')
        
        # Drop the old id column
        op.drop_column('students', 'id')
        
        # Rename the new column
        op.alter_column('students', 'id_new', new_column_name='id', nullable=False)
        
        # Create new primary key
        op.create_primary_key('students_pkey', 'students', ['id'])
    
    # Add created_at column if not exists
    if 'created_at' not in columns:
        op.add_column('students', sa.Column('created_at', sa.DateTime(), 
                                          nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')))
    
    # Create index on id
    op.create_index(op.f('ix_students_id'), 'students', ['id'], unique=False, if_not_exists=True)


def downgrade() -> None:
    """Downgrade schema."""
    # Add back the columns that were removed
    op.add_column('students', sa.Column('course_of_study', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.add_column('students', sa.Column('enrollment_number', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    
    # Revert the constraint changes
    op.drop_constraint('uq_students_user_id', 'students', type_='unique')
    op.create_index('ix_students_user_id', 'students', ['user_id'], unique=True)
