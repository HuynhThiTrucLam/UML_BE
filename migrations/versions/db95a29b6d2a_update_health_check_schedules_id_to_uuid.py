"""update_health_check_schedules_id_to_uuid

Revision ID: db95a29b6d2a
Revises: bc0ee20f5ffd
Create Date: 2025-04-16 11:45:45.786484

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = 'db95a29b6d2a'
down_revision: Union[str, None] = 'bc0ee20f5ffd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create the uuid-ossp extension if it doesn't exist
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    
    # Check if the table exists
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    if 'health_check_schedules' in inspector.get_table_names():
        # Get column information
        columns = inspector.get_columns('health_check_schedules')
        id_column = next((col for col in columns if col['name'] == 'id'), None)
        
        # Check if id column exists and is not UUID type
        if id_column and not isinstance(id_column['type'], sa.dialects.postgresql.UUID):
            # First, identify and drop all foreign keys that reference health_check_schedules.id
            for table_name in inspector.get_table_names():
                for fk in inspector.get_foreign_keys(table_name):
                    if fk.get('referred_table') == 'health_check_schedules' and 'id' in fk.get('referred_columns', []):
                        op.drop_constraint(fk.get('name'), table_name, type_='foreignkey')
            
            try:
                # Drop indexes on id column first
                op.drop_index('ix_health_check_schedules_id', table_name='health_check_schedules')
            except Exception as e:
                print(f"Info: ix_health_check_schedules_id index might not exist: {e}")
            
            # Create a temporary column with UUID type
            op.add_column('health_check_schedules', sa.Column('id_new', sa.dialects.postgresql.UUID(), nullable=True))
            
            # Generate UUIDs for existing rows
            op.execute("""
                UPDATE health_check_schedules 
                SET id_new = uuid_generate_v4()
            """)
            
            # Drop the primary key constraint
            op.drop_constraint('health_check_schedules_pkey', 'health_check_schedules', type_='primary')
            
            # Drop old id column
            op.drop_column('health_check_schedules', 'id')
            
            # Rename new column and make it primary key
            op.alter_column('health_check_schedules', 'id_new', new_column_name='id', nullable=False)
            op.create_primary_key('health_check_schedules_pkey', 'health_check_schedules', ['id'])
            
            # Recreate index
            op.create_index(op.f('ix_health_check_schedules_id'), 'health_check_schedules', ['id'], unique=False)
            
            # Recreate foreign keys that were dropped
            # This would need to be customized based on your database structure
            # For example:
            # op.create_foreign_key('fk_some_table_health_check_schedule_id', 'some_table', 'health_check_schedules', ['health_check_schedule_id'], ['id'])


def downgrade() -> None:
    """Downgrade schema."""
    # Converting UUID back to integer is lossy, so we'll just print a warning
    print("WARNING: Downgrade from UUID to integer is not supported for health_check_schedules.id")
    pass
