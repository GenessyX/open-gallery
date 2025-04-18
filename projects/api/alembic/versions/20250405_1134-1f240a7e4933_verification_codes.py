"""verification codes

Revision ID: 1f240a7e4933
Revises: 43411c52b407
Create Date: 2025-04-05 11:34:45.150605

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

import open_gallery.persistence.type_decorators

# revision identifiers, used by Alembic.
revision: str = "1f240a7e4933"
down_revision: str | None = "43411c52b407"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "verification_codes",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("code", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            open_gallery.persistence.type_decorators.datetime.UTCDateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "code"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("verification_codes")
    # ### end Alembic commands ###
