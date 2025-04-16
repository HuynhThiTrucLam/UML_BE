#!/bin/bash

# Create a completely new schema for personal_infor_documents instead of trying to modify the existing one
echo "Creating a fresh migration for personal_infor_document schema..."

# First get the ID of the merge head, which should be the latest migration
MERGE_HEAD=$(alembic heads | head -1 | awk '{print $1}')
echo "Current head migration is: $MERGE_HEAD"

# Create a new migration file
cat > "migrations/versions/fresh_personal_infor_documents.py" << EOF
"""fresh_personal_infor_documents

Revision ID: $(uuidgen | tr -d '-' | cut -c1-12)
Revises: $MERGE_HEAD
Create Date: $(date +"%Y-%m-%d %H:%M:%S.%3N")

"""
from alembic import op
import sqlalchemy as sa
import uuid


# revision identifiers, used by Alembic.
revision = '$(uuidgen | tr -d '-' | cut -c1-12)'
down_revision = '$MERGE_HEAD'
branch_labels = None
depends_on = None


def upgrade():
    # First, we drop any existing personal_infor_documents table (if it exists) to start fresh
    try:
        op.drop_table('personal_infor_documents')
    except Exception as e:
        print(f"Drop table error (can be ignored if table doesn't exist): {e}")
    
    # Create new table with the updated schema
    op.create_table('personal_infor_documents',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=True),
        sa.Column('full_name', sa.String(), nullable=True),
        sa.Column('date_of_birth', sa.String(), nullable=True),
        sa.Column('gender', sa.String(), nullable=True),
        sa.Column('address', sa.String(), nullable=True),
        sa.Column('identity_number', sa.String(), nullable=True),
        sa.Column('identity_img_front', sa.String(), nullable=True),
        sa.Column('identity_img_back', sa.String(), nullable=True),
        sa.Column('avatar', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='personal_infor_documents_user_id_fkey'),
        sa.PrimaryKeyConstraint('id', name='personal_infor_documents_pkey')
    )
    op.create_index(op.f('ix_personal_infor_documents_id'), 'personal_infor_documents', ['id'], unique=False)


def downgrade():
    # Drop the new table
    op.drop_index(op.f('ix_personal_infor_documents_id'), table_name='personal_infor_documents')
    op.drop_table('personal_infor_documents')
    
    # Create old personal_documents table (with original schema)
    op.create_table('personal_documents',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.INTEGER(), nullable=True),
        sa.Column('document_type', sa.String(), nullable=True),
        sa.Column('document_url', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='personal_documents_user_id_fkey'),
        sa.PrimaryKeyConstraint('id', name='personal_documents_pkey')
    )
    op.create_index(op.f('ix_personal_documents_id'), 'personal_documents', ['id'], unique=False)
EOF

echo "Fresh migration created successfully."
echo "You can now run 'alembic upgrade head' to apply the migration."