"""replace_license_type_id_with_course_id_in_health_check_schedules

Revision ID: 14c350b7c896
Revises: b6373fc66fb2
Create Date: 2025-04-20 13:43:06.864303

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '14c350b7c896'
down_revision: Union[str, None] = 'b6373fc66fb2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # First, add the new course_id column
    op.add_column('health_check_schedules', sa.Column('course_id', postgresql.UUID(), nullable=True))
    
    # Create a temporary table to store the mapping between license_type_id and course_id
    # Note: We need to use raw SQL for this part of the migration
    conn = op.get_bind()
    
    # For each health_check_schedule, find a course with matching license_type_id
    # and update the course_id column
    conn.execute("""
        UPDATE health_check_schedules hs
        SET course_id = (
            SELECT c.id
            FROM courses c
            WHERE c.license_type_id = hs.license_type_id
            LIMIT 1
        )
    """)
    
    # Now make the course_id column not nullable
    op.alter_column('health_check_schedules', 'course_id', nullable=False)
    
    # Create a foreign key constraint on course_id
    op.create_foreign_key(
        'fk_health_check_schedules_course_id', 
        'health_check_schedules', 
        'courses', 
        ['course_id'], 
        ['id'], 
        ondelete='CASCADE'
    )
    
    # Create an index on course_id
    op.create_index(
        'ix_health_check_schedules_course_id', 
        'health_check_schedules', 
        ['course_id']
    )
    
    # Drop the old license_type_id column and its constraints
    op.drop_constraint(
        'fk_health_check_schedules_license_type_id', 
        'health_check_schedules', 
        type_='foreignkey'
    )
    op.drop_index('ix_health_check_schedules_license_type_id', 'health_check_schedules')
    op.drop_column('health_check_schedules', 'license_type_id')


def downgrade() -> None:
    """Downgrade schema."""
    # First, add the license_type_id column back
    op.add_column(
        'health_check_schedules', 
        sa.Column('license_type_id', postgresql.UUID(), nullable=True)
    )
    
    # For each health_check_schedule, get the license_type_id from the associated course
    conn = op.get_bind()
    conn.execute("""
        UPDATE health_check_schedules hs
        SET license_type_id = (
            SELECT c.license_type_id
            FROM courses c
            WHERE c.id = hs.course_id
        )
    """)
    
    # Make license_type_id not nullable
    op.alter_column('health_check_schedules', 'license_type_id', nullable=False)
    
    # Create a foreign key constraint on license_type_id
    op.create_foreign_key(
        'fk_health_check_schedules_license_type_id', 
        'health_check_schedules', 
        'license_types', 
        ['license_type_id'], 
        ['id'], 
        ondelete='CASCADE'
    )
    
    # Create an index on license_type_id
    op.create_index(
        'ix_health_check_schedules_license_type_id', 
        'health_check_schedules', 
        ['license_type_id']
    )
    
    # Drop the course_id column and its constraints
    op.drop_constraint(
        'fk_health_check_schedules_course_id', 
        'health_check_schedules', 
        type_='foreignkey'
    )
    op.drop_index('ix_health_check_schedules_course_id', 'health_check_schedules')
    op.drop_column('health_check_schedules', 'course_id')
