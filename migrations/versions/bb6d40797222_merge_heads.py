"""merge heads

Revision ID: bb6d40797222
Revises: 392b9b727edb, a3092b36da52
Create Date: 2025-04-16 13:57:22.705378

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bb6d40797222"
down_revision: Union[str, None] = ("392b9b727edb", "a3092b36da52")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
