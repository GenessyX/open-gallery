"""user refersh tokens

Revision ID: aa0b1763820a
Revises: 34bbcde2a9a3
Create Date: 2025-04-05 10:46:08.337458

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

import open_gallery.persistence.type_decorators

# revision identifiers, used by Alembic.
revision: str = "aa0b1763820a"
down_revision: str | None = "34bbcde2a9a3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "refresh_tokens",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("token_hash", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            open_gallery.persistence.type_decorators.datetime.UTCDateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "token_hash"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("refresh_tokens")
    # ### end Alembic commands ###
