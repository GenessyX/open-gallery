"""users

Revision ID: 34bbcde2a9a3
Revises:
Create Date: 2025-03-30 15:13:38.076069

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

import open_gallery.persistence.type_decorators

# revision identifiers, used by Alembic.
revision: str = "34bbcde2a9a3"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
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
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("role", open_gallery.persistence.type_decorators.identity.UserRoleTypeImpl(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")
    # ### end Alembic commands ###
