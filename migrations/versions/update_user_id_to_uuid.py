"""update_user_id_to_uuid_in_related_tables

Revision ID: 9ca27d9e8f3c
Revises: 30a6a777c348
Create Date: 2025-04-16 14:30:00.000000

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

# revision identifiers, used by Alembic.
revision: str = "9ca27d9e8f3c"
down_revision: Union[str, None] = "30a6a777c348"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade the database to use UUID for user_id columns."""

    # Step 1: Drop all foreign key constraints
    op.execute("ALTER TABLE students DROP CONSTRAINT students_user_id_fkey")
    op.execute("ALTER TABLE staffs DROP CONSTRAINT staffs_user_id_fkey")
    op.execute("ALTER TABLE complaints DROP CONSTRAINT complaints_user_id_fkey")
    op.execute(
        "ALTER TABLE personal_infor_documents DROP CONSTRAINT personal_infor_documents_user_id_fkey"
    )

    # Step 2: Add temporary UUID columns to all tables that reference users.id
    op.execute(
        "ALTER TABLE students ADD COLUMN temp_user_id uuid DEFAULT gen_random_uuid()"
    )
    op.execute(
        "ALTER TABLE staffs ADD COLUMN temp_user_id uuid DEFAULT gen_random_uuid()"
    )
    op.execute(
        "ALTER TABLE complaints ADD COLUMN temp_user_id uuid DEFAULT gen_random_uuid()"
    )
    op.execute(
        "ALTER TABLE personal_infor_documents ADD COLUMN temp_user_id uuid DEFAULT gen_random_uuid()"
    )

    # Step 3: Generate UUIDs for existing user IDs
    op.execute("ALTER TABLE users ADD COLUMN temp_id uuid DEFAULT gen_random_uuid()")

    # Step 4: Create a mapping table to store the relationships between old integer IDs and new UUIDs
    op.execute(
        """
        CREATE TEMPORARY TABLE id_mapping (
            old_id integer PRIMARY KEY,
            new_id uuid NOT NULL
        )
    """
    )

    # Step 5: Fill the mapping table
    op.execute(
        """
        INSERT INTO id_mapping (old_id, new_id)
        SELECT id, temp_id FROM users
    """
    )

    # Step 6: Update the temporary columns in related tables using the mapping
    op.execute(
        """
        UPDATE students
        SET temp_user_id = id_mapping.new_id
        FROM id_mapping
        WHERE students.user_id = id_mapping.old_id
    """
    )

    op.execute(
        """
        UPDATE staffs
        SET temp_user_id = id_mapping.new_id
        FROM id_mapping
        WHERE staffs.user_id = id_mapping.old_id
    """
    )

    op.execute(
        """
        UPDATE complaints
        SET temp_user_id = id_mapping.new_id
        FROM id_mapping
        WHERE complaints.user_id = id_mapping.old_id
    """
    )

    op.execute(
        """
        UPDATE personal_infor_documents
        SET temp_user_id = id_mapping.new_id
        FROM id_mapping
        WHERE personal_infor_documents.user_id = id_mapping.old_id
    """
    )

    # Step 7: Drop the primary key constraint before adding a new one on users table
    op.execute("ALTER TABLE users DROP CONSTRAINT users_pkey")

    # Step 8: Create a new primary key on users.temp_id
    op.execute("ALTER TABLE users ADD PRIMARY KEY (temp_id)")

    # Step 9: Drop old id column and rename temp_id to id in users table
    op.execute("ALTER TABLE users DROP COLUMN id")
    op.execute("ALTER TABLE users RENAME COLUMN temp_id TO id")

    # Step 10: Drop old user_id columns and rename temp_user_id in related tables
    op.execute("ALTER TABLE students DROP COLUMN user_id")
    op.execute("ALTER TABLE students RENAME COLUMN temp_user_id TO user_id")

    op.execute("ALTER TABLE staffs DROP COLUMN user_id")
    op.execute("ALTER TABLE staffs RENAME COLUMN temp_user_id TO user_id")

    op.execute("ALTER TABLE complaints DROP COLUMN user_id")
    op.execute("ALTER TABLE complaints RENAME COLUMN temp_user_id TO user_id")

    op.execute("ALTER TABLE personal_infor_documents DROP COLUMN user_id")
    op.execute(
        "ALTER TABLE personal_infor_documents RENAME COLUMN temp_user_id TO user_id"
    )

    # Step 11: Recreate indexes
    op.execute("CREATE INDEX ix_users_id ON users (id)")

    # Step 12: Recreate foreign key constraints
    op.execute(
        "ALTER TABLE students ADD CONSTRAINT students_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id)"
    )
    op.execute(
        "ALTER TABLE staffs ADD CONSTRAINT staffs_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id)"
    )
    op.execute(
        "ALTER TABLE complaints ADD CONSTRAINT complaints_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id)"
    )
    op.execute(
        "ALTER TABLE personal_infor_documents ADD CONSTRAINT personal_infor_documents_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id)"
    )


def downgrade() -> None:
    """Downgrade the database back to integer for user_id columns."""
    # This is a complex migration to reverse and would require similar steps in reverse
    # Not implementing full downgrade as it's risky with data loss
    pass
