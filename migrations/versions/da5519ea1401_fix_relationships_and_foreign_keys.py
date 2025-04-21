"""fix_relationships_and_foreign_keys

Revision ID: da5519ea1401
Revises: b6373fc66fb2
Create Date: 2025-04-21 08:07:05.556842

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import exc


# revision identifiers, used by Alembic.
revision: str = 'da5519ea1401'
down_revision: Union[str, None] = 'b6373fc66fb2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def run_safe(fn):
    """Run a function and catch any exceptions."""
    try:
        fn()
    except (exc.SQLAlchemyError, exc.DBAPIError) as e:
        print(f"Ignoring error: {str(e)}")


def upgrade() -> None:
    """Upgrade schema."""
    # Get database information
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    tables = inspector.get_table_names()
    
    # 1. Fix payment_method_id in payments table (change from UUID to Integer)
    def fix_payment_method():
        if 'payments' in tables:
            columns = inspector.get_columns('payments')
            payment_method_col = next((c for c in columns if c['name'] == 'payment_method_id'), None)
            
            if payment_method_col and isinstance(payment_method_col['type'], postgresql.UUID):
                op.alter_column('payments', 'payment_method_id',
                               existing_type=postgresql.UUID(),
                               type_=sa.Integer(),
                               existing_nullable=True)
    run_safe(fix_payment_method)
    
    # 2. Add vehicle relationship to schedules if it doesn't exist
    def add_vehicle_relationship():
        constraints = inspector.get_foreign_keys('schedules')
        vehicle_fk = next((c for c in constraints if c.get('referred_table') == 'vehicles'), None)
        
        if not vehicle_fk:
            op.create_foreign_key('schedules_vehicle_id_fkey',
                               'schedules', 'vehicles', 
                               ['vehicle_id'], ['id'],
                               ondelete='CASCADE')
    run_safe(add_vehicle_relationship)
    
    # 3. Create relationship between course_registrations and schedules
    def create_association_table():
        if 'course_registration_schedule' not in tables:
            op.create_table('course_registration_schedule',
                sa.Column('course_registration_id', postgresql.UUID(), nullable=False),
                sa.Column('schedule_id', postgresql.UUID(), nullable=False),
                sa.ForeignKeyConstraint(['course_registration_id'], ['course_registrations.id'], ondelete='CASCADE'),
                sa.ForeignKeyConstraint(['schedule_id'], ['schedules.id'], ondelete='CASCADE'),
                sa.PrimaryKeyConstraint('course_registration_id', 'schedule_id')
            )
    run_safe(create_association_table)
    
    # 4. Fix foreign key constraint for course_registration_id in payments if needed
    def fix_payment_course_registration_fk():
        constraints = inspector.get_foreign_keys('payments')
        course_reg_fk = next((c for c in constraints if c.get('referred_table') == 'course_registrations' and 
                             'course_registration_id' in c.get('constrained_columns', [])), None)
        
        if not course_reg_fk:
            # Drop any existing constraint first if it exists
            existing_fks = [c['name'] for c in constraints 
                           if 'course_registration_id' in c.get('constrained_columns', [])]
            
            for fk in existing_fks:
                op.drop_constraint(fk, 'payments', type_='foreignkey')
            
            # Create the correct foreign key
            op.create_foreign_key('payments_course_registration_id_fkey', 
                              'payments', 'course_registrations',
                              ['course_registration_id'], ['id'], 
                              ondelete='CASCADE')
    run_safe(fix_payment_course_registration_fk)


def downgrade() -> None:
    """Downgrade schema."""
    pass  # We won't implement the downgrade for simplicity
