from alembic import op
import sqlalchemy as sa
import uuid

"""change course id to uuid"""

from alembic import op
import sqlalchemy as sa
import uuid

# Revision identifiers, used by Alembic.
revision = '7818ddf4930a'
down_revision = 'f49e21f2e1dd'
branch_labels = None
depends_on = None



def upgrade():
    # 1. Thêm cột mới `uuid_id` tạm thời
    op.add_column('courses', sa.Column('uuid_id', sa.UUID(), nullable=True))

    # 2. Tạo UUID cho mỗi hàng (chỉ thực hiện nếu dùng script SQL thủ công)
    op.execute('UPDATE courses SET uuid_id = gen_random_uuid()')  # hoặc uuid_generate_v4()

    # 3. Drop FK constraint trước
    op.drop_constraint('course_registrations_course_id_fkey', 'course_registrations', type_='foreignkey')

    # 4. Đổi khóa ngoại bên `course_registrations` tạm sang `uuid_id`
    op.add_column('course_registrations', sa.Column('uuid_course_id', sa.UUID(), nullable=True))

    # 5. Map id cũ sang uuid mới
    op.execute("""
        UPDATE course_registrations cr
        SET uuid_course_id = c.uuid_id
        FROM courses c
        WHERE cr.course_id = c.id
    """)

    # 6. Drop FK + PK + cột cũ
    op.drop_constraint('courses_pkey', 'courses', type_='primary')
    op.drop_column('courses', 'id')
    op.drop_column('course_registrations', 'course_id')

    # 7. Đổi tên uuid cột
    op.alter_column('courses', 'uuid_id', new_column_name='id')
    op.alter_column('course_registrations', 'uuid_course_id', new_column_name='course_id')

    # 8. Recreate PK + FK
    op.create_primary_key('courses_pkey', 'courses', ['id'])
    op.create_foreign_key(
        'course_registrations_course_id_fkey',
        'course_registrations', 'courses',
        ['course_id'], ['id'],
        ondelete='CASCADE'
    )
