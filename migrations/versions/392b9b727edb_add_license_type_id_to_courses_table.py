"""add license_type_id to courses table

Revision ID: 392b9b727edb
Revises: e8d660349145
Create Date: 2025-04-16 13:51:59.967353

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '392b9b727edb'
down_revision: Union[str, None] = 'e8d660349145'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_student_health_checks_id', table_name='student_health_checks')
    op.drop_table('student_health_checks')
    op.alter_column('absent_forms', 'student_id',
               existing_type=sa.UUID(),
               type_=sa.Integer(),
               nullable=True)
    op.drop_constraint('absent_forms_student_id_fkey', 'absent_forms', type_='foreignkey')
    op.create_foreign_key(None, 'absent_forms', 'students', ['student_id'], ['id'])
    op.alter_column('course_registrations', 'student_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.create_index(op.f('ix_course_registrations_id'), 'course_registrations', ['id'], unique=False)
    op.drop_constraint('course_registrations_student_id_fkey', 'course_registrations', type_='foreignkey')
    op.drop_constraint('course_registrations_course_id_fkey', 'course_registrations', type_='foreignkey')
    op.create_foreign_key(None, 'course_registrations', 'students', ['student_id'], ['id'])
    op.create_foreign_key(None, 'course_registrations', 'courses', ['course_id'], ['id'])
    op.add_column('courses', sa.Column('license_type_id', sa.UUID(), nullable=False))
    op.alter_column('courses', 'course_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.create_index(op.f('ix_courses_id'), 'courses', ['id'], unique=False)
    op.create_index(op.f('ix_courses_license_type_id'), 'courses', ['license_type_id'], unique=False)
    op.create_foreign_key(None, 'courses', 'license_types', ['license_type_id'], ['id'], ondelete='CASCADE')
    op.drop_column('courses', 'description')
    op.alter_column('exam_results', 'student_id',
               existing_type=sa.UUID(),
               type_=sa.Integer(),
               nullable=True)
    op.drop_constraint('exam_results_student_id_fkey', 'exam_results', type_='foreignkey')
    op.create_foreign_key(None, 'exam_results', 'students', ['student_id'], ['id'])
    op.alter_column('health_check_documents', 'health_check_id',
               existing_type=sa.INTEGER(),
               type_=sa.UUID(),
               existing_nullable=False)
    op.create_index(op.f('ix_health_check_documents_student_id'), 'health_check_documents', ['student_id'], unique=False)
    op.create_foreign_key(None, 'health_check_documents', 'health_check_schedules', ['health_check_id'], ['id'], ondelete='CASCADE')
    op.drop_column('health_check_schedules', 'scheduled_date')
    op.alter_column('license_types', 'type_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_constraint('license_types_type_name_key', 'license_types', type_='unique')
    op.drop_column('license_types', 'description')
    op.alter_column('licenses', 'license_type_id',
               existing_type=sa.UUID(),
               type_=sa.Integer(),
               existing_nullable=True)
    op.alter_column('licenses', 'student_id',
               existing_type=sa.UUID(),
               type_=sa.Integer(),
               nullable=True)
    op.drop_constraint('licenses_student_id_fkey', 'licenses', type_='foreignkey')
    op.create_foreign_key(None, 'licenses', 'students', ['student_id'], ['id'])
    op.alter_column('payments', 'student_id',
               existing_type=sa.UUID(),
               type_=sa.Integer(),
               nullable=True)
    op.drop_constraint('payments_student_id_fkey', 'payments', type_='foreignkey')
    op.create_foreign_key(None, 'payments', 'students', ['student_id'], ['id'])
    op.drop_index('ix_students_user_id', table_name='students')
    op.create_unique_constraint(None, 'students', ['user_id'])
    op.drop_column('students', 'course_of_study')
    op.drop_column('students', 'enrollment_number')
    op.add_column('users', sa.Column('user_name', sa.String(), nullable=False))
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=False))
    op.create_index(op.f('ix_users_phone_number'), 'users', ['phone_number'], unique=False)
    op.create_index(op.f('ix_users_user_name'), 'users', ['user_name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_user_name'), table_name='users')
    op.drop_index(op.f('ix_users_phone_number'), table_name='users')
    op.drop_column('users', 'phone_number')
    op.drop_column('users', 'user_name')
    op.add_column('students', sa.Column('enrollment_number', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('students', sa.Column('course_of_study', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'students', type_='unique')
    op.create_index('ix_students_user_id', 'students', ['user_id'], unique=True)
    op.drop_constraint(None, 'payments', type_='foreignkey')
    op.create_foreign_key('payments_student_id_fkey', 'payments', 'students', ['student_id'], ['id'], ondelete='CASCADE')
    op.alter_column('payments', 'student_id',
               existing_type=sa.Integer(),
               type_=sa.UUID(),
               nullable=False)
    op.drop_constraint(None, 'licenses', type_='foreignkey')
    op.create_foreign_key('licenses_student_id_fkey', 'licenses', 'students', ['student_id'], ['id'], ondelete='CASCADE')
    op.alter_column('licenses', 'student_id',
               existing_type=sa.Integer(),
               type_=sa.UUID(),
               nullable=False)
    op.alter_column('licenses', 'license_type_id',
               existing_type=sa.Integer(),
               type_=sa.UUID(),
               existing_nullable=True)
    op.add_column('license_types', sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_unique_constraint('license_types_type_name_key', 'license_types', ['type_name'])
    op.alter_column('license_types', 'type_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.add_column('health_check_schedules', sa.Column('scheduled_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'health_check_documents', type_='foreignkey')
    op.drop_index(op.f('ix_health_check_documents_student_id'), table_name='health_check_documents')
    op.alter_column('health_check_documents', 'health_check_id',
               existing_type=sa.UUID(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.drop_constraint(None, 'exam_results', type_='foreignkey')
    op.create_foreign_key('exam_results_student_id_fkey', 'exam_results', 'students', ['student_id'], ['id'], ondelete='CASCADE')
    op.alter_column('exam_results', 'student_id',
               existing_type=sa.Integer(),
               type_=sa.UUID(),
               nullable=False)
    op.add_column('courses', sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'courses', type_='foreignkey')
    op.drop_index(op.f('ix_courses_license_type_id'), table_name='courses')
    op.drop_index(op.f('ix_courses_id'), table_name='courses')
    op.alter_column('courses', 'course_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('courses', 'license_type_id')
    op.drop_constraint(None, 'course_registrations', type_='foreignkey')
    op.drop_constraint(None, 'course_registrations', type_='foreignkey')
    op.create_foreign_key('course_registrations_course_id_fkey', 'course_registrations', 'courses', ['course_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('course_registrations_student_id_fkey', 'course_registrations', 'students', ['student_id'], ['id'], ondelete='CASCADE')
    op.drop_index(op.f('ix_course_registrations_id'), table_name='course_registrations')
    op.alter_column('course_registrations', 'student_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.drop_constraint(None, 'absent_forms', type_='foreignkey')
    op.create_foreign_key('absent_forms_student_id_fkey', 'absent_forms', 'students', ['student_id'], ['id'], ondelete='CASCADE')
    op.alter_column('absent_forms', 'student_id',
               existing_type=sa.Integer(),
               type_=sa.UUID(),
               nullable=False)
    op.create_table('student_health_checks',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('status', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('remarks', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('student_id', sa.UUID(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], name='student_health_checks_student_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='student_health_checks_pkey')
    )
    op.create_index('ix_student_health_checks_id', 'student_health_checks', ['id'], unique=False)
    # ### end Alembic commands ###
