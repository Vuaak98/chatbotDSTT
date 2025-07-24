"""apply_recent_model_changes

Revision ID: 57fce4e59ffd
Revises: b3f8436f0f59
Create Date: 2025-05-14 10:30:29.311451

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '57fce4e59ffd'
down_revision: Union[str, None] = 'b3f8436f0f59'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
