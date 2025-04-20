"""update_health_check_documents_id_to_uuid

Revision ID: 9d702150479b
Revises: 97b475e893cc
Create Date: 2025-04-18 10:55:05.906576

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = '9d702150479b'
down_revision: Union[str, None] = '97b475e893cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Using raw SQL for more control over the migration process
    op.execute("""
    DO $$
    DECLARE
      constraint_exists boolean;
    BEGIN
        -- Check if the foreign key constraint exists
        SELECT EXISTS (
            SELECT 1
            FROM pg_constraint
            WHERE conname = 'health_check_documents_health_check_id_fkey'
        ) INTO constraint_exists;
        
        -- Create a temporary column with the correct UUID type
        ALTER TABLE health_check_documents ADD COLUMN health_check_id_new UUID;
        
        -- Use a join to get the correct UUID values from the health_check_schedules table
        UPDATE health_check_documents AS hcd
        SET health_check_id_new = hcs.id
        FROM health_check_schedules AS hcs
        WHERE hcd.health_check_id::text = hcs.id::text;
        
        -- Drop the foreign key constraint if it exists
        IF constraint_exists THEN
            ALTER TABLE health_check_documents DROP CONSTRAINT health_check_documents_health_check_id_fkey;
        END IF;
        
        -- Drop the old column
        ALTER TABLE health_check_documents DROP COLUMN health_check_id;
        
        -- Rename the new column to the original name
        ALTER TABLE health_check_documents RENAME COLUMN health_check_id_new TO health_check_id;
        
        -- Make it not nullable
        ALTER TABLE health_check_documents ALTER COLUMN health_check_id SET NOT NULL;
        
        -- Re-create the foreign key constraint with the proper type
        ALTER TABLE health_check_documents 
        ADD CONSTRAINT health_check_documents_health_check_id_fkey 
        FOREIGN KEY (health_check_id) 
        REFERENCES health_check_schedules(id) ON DELETE CASCADE;
        
        -- Create an index on the column
        CREATE INDEX IF NOT EXISTS ix_health_check_documents_health_check_id ON health_check_documents(health_check_id);
    END;
    $$;
    """)


def downgrade() -> None:
    """Downgrade schema."""
    # This is a complex migration to undo, as we would need to map UUIDs back to integers.
    # Since this is fixing a data type mismatch, a proper downgrade would require
    # knowing the original integer values which we no longer have.
    op.execute("""
    -- Just a placeholder for downgrade, actual implementation would depend on having the original ID mapping
    -- which is not feasible in this case.
    SELECT 'Downgrade not supported for this migration'::text;
    """)
    pass
