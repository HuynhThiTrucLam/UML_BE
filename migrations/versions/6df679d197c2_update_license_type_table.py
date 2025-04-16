"""update_license_type_table

Revision ID: 6df679d197c2
Revises: e2e14b87215a
Create Date: 2025-04-16 11:29:15.885539

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid


# revision identifiers, used by Alembic.
revision: str = '6df679d197c2'
down_revision: Union[str, None] = 'e2e14b87215a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create the uuid-ossp extension if it doesn't exist
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    
    # Check if the table exists
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    if 'license_types' not in inspector.get_table_names():
        # Create the license_types table with all required columns and constraints
        op.create_table(
            'license_types',
            sa.Column('id', postgresql.UUID(), nullable=False, server_default=sa.text('uuid_generate_v4()')),
            sa.Column('type_name', sa.String(), nullable=False),
            sa.Column('age_requirement', sa.String(), nullable=False),
            sa.Column('health_requirements', sa.String(), nullable=False),
            sa.Column('training_duration', sa.Integer(), nullable=False),
            sa.Column('fee', sa.Integer(), nullable=False),
            sa.PrimaryKeyConstraint('id'),
            sa.CheckConstraint('training_duration > 0', name='check_training_duration_positive'),
            sa.CheckConstraint('fee >= 0', name='check_fee_non_negative')
        )
        op.create_index(op.f('ix_license_types_id'), 'license_types', ['id'], unique=False)
        op.create_index(op.f('ix_license_types_type_name'), 'license_types', ['type_name'], unique=True)
    else:
        # If the table exists, update it to match the model
        
        # Check for UUID column type and update if necessary
        columns = inspector.get_columns('license_types')
        column_names = [col['name'] for col in columns]
        column_types = {col['name']: col['type'] for col in columns}
        
        # Add missing columns
        required_columns = ['id', 'type_name', 'age_requirement', 'health_requirements', 'training_duration', 'fee']
        
        for col_name in required_columns:
            if col_name not in column_names:
                if col_name == 'id':
                    op.add_column('license_types', sa.Column('id', postgresql.UUID(), nullable=False, server_default=sa.text('uuid_generate_v4()')))
                elif col_name == 'type_name':
                    op.add_column('license_types', sa.Column('type_name', sa.String(), nullable=False))
                elif col_name == 'age_requirement':
                    op.add_column('license_types', sa.Column('age_requirement', sa.String(), nullable=False))
                elif col_name == 'health_requirements':
                    op.add_column('license_types', sa.Column('health_requirements', sa.String(), nullable=False))
                elif col_name == 'training_duration':
                    op.add_column('license_types', sa.Column('training_duration', sa.Integer(), nullable=False))
                elif col_name == 'fee':
                    op.add_column('license_types', sa.Column('fee', sa.Integer(), nullable=False))
        
        # Add missing indexes
        indexes = inspector.get_indexes('license_types')
        index_names = [idx['name'] for idx in indexes]
        
        if 'ix_license_types_id' not in index_names:
            op.create_index(op.f('ix_license_types_id'), 'license_types', ['id'], unique=False)
        
        if 'ix_license_types_type_name' not in index_names:
            op.create_index(op.f('ix_license_types_type_name'), 'license_types', ['type_name'], unique=True)
        
        # Add constraints
        try:
            op.create_check_constraint('check_training_duration_positive', 'license_types', 'training_duration > 0')
        except:
            # Constraint may already exist
            pass
        
        try:
            op.create_check_constraint('check_fee_non_negative', 'license_types', 'fee >= 0')
        except:
            # Constraint may already exist
            pass


def downgrade() -> None:
    """Downgrade schema."""
    # Drop constraints first
    try:
        op.drop_constraint('check_training_duration_positive', 'license_types', type_='check')
    except:
        pass
    
    try:
        op.drop_constraint('check_fee_non_negative', 'license_types', type_='check')
    except:
        pass
    
    # Drop indexes
    try:
        op.drop_index(op.f('ix_license_types_type_name'), table_name='license_types')
    except:
        pass
    
    try:
        op.drop_index(op.f('ix_license_types_id'), table_name='license_types')
    except:
        pass
    
    # Check if the table was created by this migration, and if so, drop it
    conn = op.get_bind()
    if 'license_types' in sa.inspect(conn).get_table_names():
        op.drop_table('license_types')
