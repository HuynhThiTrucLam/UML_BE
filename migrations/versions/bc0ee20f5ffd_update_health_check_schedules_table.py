"""update_health_check_schedules_table

Revision ID: bc0ee20f5ffd
Revises: 6df679d197c2
Create Date: 2025-04-16 11:34:28.871549

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = 'bc0ee20f5ffd'
down_revision: Union[str, None] = '6df679d197c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create the uuid-ossp extension if it doesn't exist
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    
    # Check if the table exists
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    # First we need to handle the license_types table and its dependencies
    if 'license_types' in inspector.get_table_names():
        # Check the type of the id column in license_types
        license_types_columns = inspector.get_columns('license_types')
        id_column = next((col for col in license_types_columns if col['name'] == 'id'), None)
        
        # If id column exists and is not UUID type, we need to modify it
        if id_column and not isinstance(id_column['type'], postgresql.UUID):
            try:
                # First, identify and drop all foreign keys that reference license_types.id
                
                # Check if licenses table exists and drop its FK to license_types
                if 'licenses' in inspector.get_table_names():
                    for fk in inspector.get_foreign_keys('licenses'):
                        if fk.get('referred_table') == 'license_types' and 'id' in fk.get('referred_columns', []):
                            op.drop_constraint(fk.get('name'), 'licenses', type_='foreignkey')
                    
                    # Update the column type in licenses table too
                    license_columns = inspector.get_columns('licenses')
                    if any(col['name'] == 'license_type_id' for col in license_columns):
                        # First drop the column
                        op.drop_column('licenses', 'license_type_id')
                        # Then recreate it with UUID type
                        op.add_column('licenses', sa.Column('license_type_id', postgresql.UUID(), nullable=True))
                
                # Check if health_check_schedules table exists and drop its FK to license_types
                if 'health_check_schedules' in inspector.get_table_names():
                    for fk in inspector.get_foreign_keys('health_check_schedules'):
                        if fk.get('referred_table') == 'license_types' and 'id' in fk.get('referred_columns', []):
                            op.drop_constraint(fk.get('name'), 'health_check_schedules', type_='foreignkey')
                
                # Now modify the license_types table
                # Check if index exists and drop it first
                try:
                    op.drop_index('ix_license_types_id', table_name='license_types')
                except Exception as e:
                    # If index doesn't exist, continue
                    print(f"Info: ix_license_types_id index might not exist: {e}")
                    
                # Create a temporary column
                op.add_column('license_types', sa.Column('id_new', postgresql.UUID(), nullable=True))
                
                # Generate UUID for existing rows
                op.execute("""
                    UPDATE license_types 
                    SET id_new = uuid_generate_v4()
                """)
                
                # Drop the primary key constraint
                op.drop_constraint('license_types_pkey', 'license_types', type_='primary')
                
                # Drop old id column
                op.drop_column('license_types', 'id')
                
                # Rename new column and make it primary key
                op.alter_column('license_types', 'id_new', new_column_name='id', nullable=False)
                op.create_primary_key('license_types_pkey', 'license_types', ['id'])
                
                # Create the index
                op.create_index(op.f('ix_license_types_id'), 'license_types', ['id'], unique=False)
                
                # Now add back the foreign key constraints
                # For licenses table
                if 'licenses' in inspector.get_table_names():
                    try:
                        op.create_foreign_key(
                            'licenses_license_type_id_fkey',
                            'licenses',
                            'license_types',
                            ['license_type_id'],
                            ['id']
                        )
                    except Exception as e:
                        print(f"Warning: Could not create foreign key for licenses: {e}")
            except Exception as e:
                # If any error occurs during license_types modification, log it and continue
                print(f"Error modifying license_types table: {e}")
                conn.execute("ROLLBACK")
                # Get a fresh connection
                conn = op.get_bind()
                inspector = sa.inspect(conn)
    
    # Now handle the health_check_schedules table
    try:
        if 'health_check_schedules' not in inspector.get_table_names():
            # Create the health_check_schedules table with all required columns and constraints
            op.create_table(
                'health_check_schedules',
                sa.Column('id', postgresql.UUID(), nullable=False, server_default=sa.text('uuid_generate_v4()')),
                sa.Column('license_type_id', postgresql.UUID(), nullable=False),
                sa.Column('address', sa.String(), nullable=False),
                sa.Column('scheduled_datetime', sa.DateTime(), nullable=False),
                sa.Column('description', sa.String(), nullable=True),
                sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
                sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'), onupdate=sa.text('CURRENT_TIMESTAMP')),
                sa.ForeignKeyConstraint(['license_type_id'], ['license_types.id'], ),
                sa.PrimaryKeyConstraint('id'),
                sa.CheckConstraint('scheduled_datetime > CURRENT_TIMESTAMP', name='check_schedule_in_future')
            )
            op.create_index(op.f('ix_health_check_schedules_id'), 'health_check_schedules', ['id'], unique=False)
            op.create_index(op.f('ix_health_check_schedules_license_type_id'), 'health_check_schedules', ['license_type_id'], unique=False)
            op.create_index(op.f('ix_health_check_schedules_address'), 'health_check_schedules', ['address'], unique=False)
        else:
            # If the table exists, update it to match the model
            
            # Check columns and add missing ones
            columns = inspector.get_columns('health_check_schedules')
            column_names = [col['name'] for col in columns]
            column_types = {col['name']: col['type'] for col in columns}
            
            # Check if license_type_id is the right type (UUID)
            if 'license_type_id' in column_names and not isinstance(column_types['license_type_id'], postgresql.UUID):
                # Drop any foreign key constraints first
                for fk in inspector.get_foreign_keys('health_check_schedules'):
                    if 'license_type_id' in fk.get('constrained_columns', []):
                        op.drop_constraint(fk.get('name'), 'health_check_schedules', type_='foreignkey')
                
                # Drop the column and recreate it with UUID type
                op.drop_column('health_check_schedules', 'license_type_id')
                op.add_column('health_check_schedules', sa.Column('license_type_id', postgresql.UUID(), nullable=False))
            
            # Add missing columns
            required_columns = ['id', 'license_type_id', 'address', 'scheduled_datetime', 'description', 'created_at', 'updated_at']
            
            for col_name in required_columns:
                if col_name not in column_names:
                    if col_name == 'id':
                        op.add_column('health_check_schedules', sa.Column('id', postgresql.UUID(), nullable=False, server_default=sa.text('uuid_generate_v4()')))
                    elif col_name == 'license_type_id':
                        op.add_column('health_check_schedules', sa.Column('license_type_id', postgresql.UUID(), nullable=False))
                    elif col_name == 'address':
                        op.add_column('health_check_schedules', sa.Column('address', sa.String(), nullable=False))
                    elif col_name == 'scheduled_datetime':
                        op.add_column('health_check_schedules', sa.Column('scheduled_datetime', sa.DateTime(), nullable=False))
                    elif col_name == 'description':
                        op.add_column('health_check_schedules', sa.Column('description', sa.String(), nullable=True))
                    elif col_name == 'created_at':
                        op.add_column('health_check_schedules', sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')))
                    elif col_name == 'updated_at':
                        op.add_column('health_check_schedules', sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')))
            
            # Add missing indexes
            indexes = inspector.get_indexes('health_check_schedules')
            index_names = [idx['name'] for idx in indexes]
            
            if 'ix_health_check_schedules_id' not in index_names:
                op.create_index(op.f('ix_health_check_schedules_id'), 'health_check_schedules', ['id'], unique=False)
            
            if 'ix_health_check_schedules_license_type_id' not in index_names:
                op.create_index(op.f('ix_health_check_schedules_license_type_id'), 'health_check_schedules', ['license_type_id'], unique=False)
            
            if 'ix_health_check_schedules_address' not in index_names:
                op.create_index(op.f('ix_health_check_schedules_address'), 'health_check_schedules', ['address'], unique=False)
            
            # Add the constraint for scheduled_datetime if it doesn't exist
            try:
                op.create_check_constraint('check_schedule_in_future', 'health_check_schedules', 'scheduled_datetime > CURRENT_TIMESTAMP')
            except Exception as e:
                # Constraint may already exist
                print(f"Info: check_schedule_in_future constraint might already exist: {e}")
            
            # Add foreign key constraint if it doesn't exist
            foreign_keys = inspector.get_foreign_keys('health_check_schedules')
            fk_names = [fk['name'] for fk in foreign_keys]
            
            # Create a name for the FK constraint
            fk_name = 'fk_health_check_schedules_license_type_id_license_types'
            if fk_name not in fk_names and not any(fk['referred_table'] == 'license_types' for fk in foreign_keys):
                try:
                    op.create_foreign_key(
                        fk_name,
                        'health_check_schedules',
                        'license_types',
                        ['license_type_id'],
                        ['id']
                    )
                except Exception as e:
                    # If we can't create the constraint, log the error and continue
                    print(f"Error creating foreign key: {e}")
    except Exception as e:
        # If any error occurs during health_check_schedules modification, log it
        print(f"Error modifying health_check_schedules table: {e}")
        conn.execute("ROLLBACK")


def downgrade() -> None:
    """Downgrade schema."""
    # Drop constraints first
    try:
        op.drop_constraint('check_schedule_in_future', 'health_check_schedules', type_='check')
    except:
        pass
    
    try:
        op.drop_constraint('fk_health_check_schedules_license_type_id_license_types', 'health_check_schedules', type_='foreignkey')
    except:
        pass
    
    # Drop indexes
    try:
        op.drop_index(op.f('ix_health_check_schedules_address'), table_name='health_check_schedules')
    except:
        pass
    
    try:
        op.drop_index(op.f('ix_health_check_schedules_license_type_id'), table_name='health_check_schedules')
    except:
        pass
    
    try:
        op.drop_index(op.f('ix_health_check_schedules_id'), table_name='health_check_schedules')
    except:
        pass
    
    # Check if the table was created by this migration, and if so, drop it
    conn = op.get_bind()
    if 'health_check_schedules' in sa.inspect(conn).get_table_names():
        op.drop_table('health_check_schedules')
