"""merge_heads

Revision ID: 991d9ae13101
Revises: 3205b0c2b431, da5519ea1401
Create Date: 2025-04-21 08:10:27.976789

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '991d9ae13101'
down_revision: Union[str, None] = ('3205b0c2b431', 'da5519ea1401')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
