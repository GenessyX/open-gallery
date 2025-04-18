"""notification related object id

Revision ID: 289d4a9d3797
Revises: 4ce61c9cd010
Create Date: 2025-04-12 18:24:38.806125

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "289d4a9d3797"
down_revision: str | None = "4ce61c9cd010"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("notifications", sa.Column("related_object_id", sa.UUID(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("notifications", "related_object_id")
    # ### end Alembic commands ###
