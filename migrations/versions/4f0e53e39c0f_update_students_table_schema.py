"""update_students_table_schema

Revision ID: 4f0e53e39c0f
Revises: db95a29b6d2a
Create Date: 2025-04-16 11:54:27.349937

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = "4f0e53e39c0f"
down_revision: Union[str, None] = "db95a29b6d2a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create the uuid-ossp extension if it doesn't exist
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    # Check if the table exists
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    if "students" in inspector.get_table_names():
        # Table exists, need to migrate from old schema to new schema

        # First check if the id column is already UUID
        columns = {c["name"]: c for c in inspector.get_columns("students")}

        # If id is not UUID type, we need to update the schema
        if not isinstance(columns.get("id", {}).get("type"), postgresql.UUID):
            # Store foreign key constraints that depend on students.id to recreate later
            dependent_fks = []
            dependent_tables = [
                "absent_forms",
                "course_registrations",
                "exam_results",
                "licenses",
                "payments",
                "student_health_checks",
                "health_check_documents",
            ]

            # Collect information about dependent foreign keys and drop them
            for table_name in dependent_tables:
                if table_name in inspector.get_table_names():
                    for fk in inspector.get_foreign_keys(table_name):
                        if fk.get("referred_table") == "students" and "id" in fk.get(
                            "referred_columns", []
                        ):
                            dependent_fks.append(
                                {
                                    "table": table_name,
                                    "name": fk["name"],
                                    "columns": fk["constrained_columns"],
                                    "referred_columns": fk["referred_columns"],
                                }
                            )
                            op.drop_constraint(
                                fk["name"], table_name, type_="foreignkey"
                            )

            # Step 1: Create temporary UUID columns
            op.add_column(
                "students", sa.Column("id_new", postgresql.UUID(), nullable=True)
            )
            op.add_column(
                "students", sa.Column("user_id_new", postgresql.UUID(), nullable=True)
            )

            # Step 2: Generate UUIDs for all existing records and create a mapping table
            op.execute(
                "CREATE TEMP TABLE student_id_mapping AS SELECT id, uuid_generate_v4() as new_id FROM students"
            )
            op.execute("CREATE INDEX ON student_id_mapping (id)")

            # Update the new ID columns using the mapping
            op.execute(
                "UPDATE students SET id_new = student_id_mapping.new_id FROM student_id_mapping WHERE students.id = student_id_mapping.id"
            )

            # Check if users table exists and if it has a UUID primary key
            users_columns = {}
            if "users" in inspector.get_table_names():
                users_columns = {c["name"]: c for c in inspector.get_columns("users")}

            # Handle user_id mapping with proper type casting
            if "users" in inspector.get_table_names() and isinstance(
                users_columns.get("id", {}).get("type"), postgresql.UUID
            ):
                # If users table has UUID primary key, create a mapping for user_id
                op.execute(
                    """
                    UPDATE students SET user_id_new = u.id 
                    FROM users u 
                    WHERE students.user_id::text = u.id::text
                """
                )
            else:
                # Generate new UUIDs for user_id
                op.execute("UPDATE students SET user_id_new = uuid_generate_v4()")

            # Step 3: Drop existing constraints and indexes on students table only
            for fk in inspector.get_foreign_keys("students"):
                op.drop_constraint(fk["name"], "students", type_="foreignkey")

            for idx in inspector.get_indexes("students"):
                op.drop_index(idx["name"], table_name="students")

            # Step 4: Drop the primary key
            op.drop_constraint("students_pkey", "students", type_="primary")

            # Step 5: Drop the old columns
            op.drop_column("students", "id")
            op.drop_column("students", "user_id")

            # Step 6: Rename the new columns
            op.alter_column("students", "id_new", new_column_name="id", nullable=False)
            op.alter_column(
                "students", "user_id_new", new_column_name="user_id", nullable=False
            )

            # Step 7: Add the created_at column if it doesn't exist
            if "created_at" not in columns:
                op.add_column(
                    "students",
                    sa.Column(
                        "created_at",
                        sa.DateTime(),
                        nullable=False,
                        server_default=sa.text("CURRENT_TIMESTAMP"),
                    ),
                )

            # Step 8: Add new fields for students table
            op.add_column(
                "students",
                sa.Column("enrollment_number", sa.String(length=50), nullable=True),
            )
            op.add_column(
                "students",
                sa.Column("course_of_study", sa.String(length=100), nullable=True),
            )

            # Step 9: Create primary key and foreign key constraints
            op.create_primary_key("students_pkey", "students", ["id"])
            op.create_foreign_key(
                "students_user_id_fkey",
                "students",
                "users",
                ["user_id"],
                ["id"],
                ondelete="CASCADE",
            )
            op.create_index(op.f("ix_students_id"), "students", ["id"], unique=False)
            op.create_index(
                op.f("ix_students_user_id"), "students", ["user_id"], unique=True
            )
            op.create_index(
                op.f("ix_students_enrollment_number"),
                "students",
                ["enrollment_number"],
                unique=True,
            )

            # Step 10: Update dependent tables with the new UUIDs
            for table_name in dependent_tables:
                if table_name in inspector.get_table_names():
                    # Add new UUID column for student_id
                    op.add_column(
                        table_name,
                        sa.Column("student_id_new", postgresql.UUID(), nullable=True),
                    )

                    # Update the new UUID column with the mapping
                    op.execute(
                        f"""
                        UPDATE {table_name} 
                        SET student_id_new = student_id_mapping.new_id 
                        FROM student_id_mapping 
                        WHERE {table_name}.student_id = student_id_mapping.id
                    """
                    )

                    # Drop the old foreign key constraint and column
                    op.drop_column(table_name, "student_id")

                    # Rename the new column
                    op.alter_column(
                        table_name,
                        "student_id_new",
                        new_column_name="student_id",
                        nullable=False,
                    )

                    # Recreate the foreign key constraint
                    op.create_foreign_key(
                        f"{table_name}_student_id_fkey",
                        table_name,
                        "students",
                        ["student_id"],
                        ["id"],
                        ondelete="CASCADE",
                    )

            # Clean up the temporary table
            op.execute("DROP TABLE student_id_mapping")

        else:
            # The table already has UUID for id, just add the new fields
            op.add_column(
                "students",
                sa.Column("enrollment_number", sa.String(length=50), nullable=True),
            )
            op.add_column(
                "students",
                sa.Column("course_of_study", sa.String(length=100), nullable=True),
            )
            op.create_index(
                op.f("ix_students_enrollment_number"),
                "students",
                ["enrollment_number"],
                unique=True,
            )

    else:
        # Create the table from scratch with all fields
        op.create_table(
            "students",
            sa.Column(
                "id",
                postgresql.UUID(),
                nullable=False,
                server_default=sa.text("uuid_generate_v4()"),
            ),
            sa.Column("user_id", postgresql.UUID(), nullable=False),
            sa.Column("enrollment_number", sa.String(length=50), nullable=True),
            sa.Column("course_of_study", sa.String(length=100), nullable=True),
            sa.Column(
                "created_at",
                sa.DateTime(),
                nullable=False,
                server_default=sa.text("CURRENT_TIMESTAMP"),
            ),
            sa.ForeignKeyConstraint(
                ["user_id"],
                ["users.id"],
                name="students_user_id_fkey",
                ondelete="CASCADE",
            ),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("user_id"),
        )
        op.create_index(op.f("ix_students_id"), "students", ["id"], unique=False)
        op.create_index(
            op.f("ix_students_user_id"), "students", ["user_id"], unique=True
        )
        op.create_index(
            op.f("ix_students_enrollment_number"),
            "students",
            ["enrollment_number"],
            unique=True,
        )


def downgrade() -> None:
    """Downgrade schema."""
    # This is a complex migration that involves multiple tables.
    # We'll drop the new columns we added and keep the UUID structure

    conn = op.get_bind()
    inspector = sa.inspect(conn)

    if "students" in inspector.get_table_names():
        columns = {c["name"]: c for c in inspector.get_columns("students")}

        # Drop indexes on new columns
        if inspector.get_indices("students"):
            indexes = inspector.get_indices("students")
            for idx in indexes:
                if idx["name"] == "ix_students_enrollment_number":
                    op.drop_index(idx["name"], table_name="students")

        # Drop the new columns
        if "enrollment_number" in columns:
            op.drop_column("students", "enrollment_number")
        if "course_of_study" in columns:
            op.drop_column("students", "course_of_study")

    # We won't revert the UUID changes as that would be too risky
    op.execute("SELECT 1")  # No-op
