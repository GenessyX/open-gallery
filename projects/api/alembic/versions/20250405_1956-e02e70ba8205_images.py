"""images

Revision ID: e02e70ba8205
Revises: 1f240a7e4933
Create Date: 2025-04-05 19:56:06.823672

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

import open_gallery.persistence.type_decorators

# revision identifiers, used by Alembic.
revision: str = "e02e70ba8205"
down_revision: str | None = "1f240a7e4933"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "images",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column(
            "created_at",
            open_gallery.persistence.type_decorators.datetime.UTCDateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            open_gallery.persistence.type_decorators.datetime.UTCDateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("path", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("images")
    # ### end Alembic commands ###
