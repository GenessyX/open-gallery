"""images uploaded_by

Revision ID: 61c920656dc6
Revises: e02e70ba8205
Create Date: 2025-04-05 20:58:09.911210

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "61c920656dc6"
down_revision: str | None = "e02e70ba8205"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "images",
        sa.Column("uploaded_by_id", sa.UUID(), nullable=False),
    )
    op.create_foreign_key(
        "images_uploaded_by_id_fkey",
        "images",
        "users",
        ["uploaded_by_id"],
        ["id"],
        ondelete="CASCADE",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "images_uploaded_by_id_fkey",
        "images",
        type_="foreignkey",
    )
    op.drop_column("images", "uploaded_by_id")
    # ### end Alembic commands ###
