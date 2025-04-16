"""add student_id foreign key to course_registrations

Revision ID: e8d660349145
Revises: 7fad0257fa5d
Create Date: 2025-04-16 13:45:16.317003

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8d660349145'
down_revision: Union[str, None] = '7fad0257fa5d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('course_registrations', sa.Column('student_id', sa.dialects.postgresql.UUID(), nullable=False))
    op.create_foreign_key('fk_course_registrations_student_id', 'course_registrations', 'students', ['student_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_course_registrations_student_id', 'course_registrations', type_='foreignkey')
    op.drop_column('course_registrations', 'student_id')
