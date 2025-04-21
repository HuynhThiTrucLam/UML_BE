"""update_course_table

Revision ID: f49e21f2e1dd
Revises: 53adc465e861
Create Date: 2025-04-16 12:24:31.690134

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision: str = "f49e21f2e1dd"
down_revision: Union[str, None] = "53adc465e861"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Get connection and inspector for examining the schema
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    # First, check if the courses table exists
    if "courses" not in inspector.get_table_names():
        # The table doesn't exist yet, so we don't need to update it
        return

    # Get the list of columns
    columns = [col["name"] for col in inspector.get_columns("courses")]

    # Add missing columns if they don't exist
    if "max_students" not in columns:
        op.add_column(
            "courses",
            sa.Column(
                "max_students", sa.Integer(), nullable=False, server_default="30"
            ),
        )

    if "current_students" not in columns:
        op.add_column(
            "courses",
            sa.Column(
                "current_students", sa.Integer(), nullable=False, server_default="0"
            ),
        )

    if "price" not in columns:
        op.add_column(
            "courses",
            sa.Column("price", sa.Integer(), nullable=False, server_default="0"),
        )

    # Add created_at if it doesn't exist
    if "created_at" not in columns:
        op.add_column(
            "courses",
            sa.Column(
                "created_at",
                sa.Date(),
                nullable=False,
                server_default=sa.func.current_date(),
            ),
        )

    # Add updated_at if it doesn't exist
    if "updated_at" not in columns:
        op.add_column(
            "courses",
            sa.Column(
                "updated_at",
                sa.Date(),
                nullable=False,
                server_default=sa.func.current_date(),
            ),
        )

    # Add status if it doesn't exist
    if "status" not in columns:
        op.add_column(
            "courses",
            sa.Column("status", sa.String(), nullable=False, server_default="active"),
        )

    # Add course_name if it doesn't exist
    if "course_name" not in columns:
        op.add_column(
            "courses",
            sa.Column(
                "course_name", sa.String(), nullable=False, server_default="New Course"
            ),
        )

    # Add start_date if it doesn't exist
    if "start_date" not in columns:
        op.add_column(
            "courses",
            sa.Column(
                "start_date",
                sa.Date(),
                nullable=False,
                server_default=sa.func.current_date(),
            ),
        )

    # Add end_date if it doesn't exist
    if "end_date" not in columns:
        op.add_column(
            "courses",
            sa.Column(
                "end_date",
                sa.Date(),
                nullable=False,
                server_default=sa.text("(current_date + interval '30 days')"),
            ),
        )

    # Get updated list of constraints
    constraints = []
    try:
        constraints = [
            con["name"] for con in inspector.get_check_constraints("courses")
        ]
    except:
        pass

    # Now try to add the constraints
    try:
        if "check_max_students_positive" not in constraints:
            op.execute(
                "ALTER TABLE courses ADD CONSTRAINT check_max_students_positive CHECK (max_students >= 0)"
            )
    except Exception as e:
        print(f"Error adding max_students constraint: {e}")

    try:
        if "check_current_students_positive" not in constraints:
            op.execute(
                "ALTER TABLE courses ADD CONSTRAINT check_current_students_positive CHECK (current_students >= 0)"
            )
    except Exception as e:
        print(f"Error adding current_students constraint: {e}")

    try:
        if "check_price_positive" not in constraints:
            op.execute(
                "ALTER TABLE courses ADD CONSTRAINT check_price_positive CHECK (price >= 0)"
            )
    except Exception as e:
        print(f"Error adding price constraint: {e}")

    try:
        if "check_course_status_valid" not in constraints:
            op.execute(
                "ALTER TABLE courses ADD CONSTRAINT check_course_status_valid CHECK (status IN ('active', 'inactive'))"
            )
    except Exception as e:
        print(f"Error adding status constraint: {e}")

    # Check if course_name is indexed
    indexes = [idx["name"] for idx in inspector.get_indexes("courses")]
    if "ix_courses_course_name" not in indexes:
        try:
            op.create_index(
                op.f("ix_courses_course_name"), "courses", ["course_name"], unique=False
            )
        except Exception as e:
            print(f"Error adding course_name index: {e}")


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    # First, check if the courses table exists
    if "courses" not in inspector.get_table_names():
        return

    # Get existing constraints
    constraints = []
    try:
        constraints = [
            con["name"] for con in inspector.get_check_constraints("courses")
        ]
    except:
        pass

    # Drop constraints if they exist
    for constraint_name in [
        "check_max_students_positive",
        "check_current_students_positive",
        "check_price_positive",
        "check_course_status_valid",
    ]:
        if constraint_name in constraints:
            try:
                op.drop_constraint(constraint_name, "courses", type_="check")
            except Exception as e:
                print(f"Error dropping constraint {constraint_name}: {e}")

    # Check if the index exists and drop it
    indexes = [idx["name"] for idx in inspector.get_indexes("courses")]
    if "ix_courses_course_name" in indexes:
        try:
            op.drop_index(op.f("ix_courses_course_name"), table_name="courses")
        except Exception as e:
            print(f"Error dropping index: {e}")
