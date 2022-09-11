"""add last few columns to posts table

Revision ID: 5381b0430501
Revises: fef59b19ba06
Create Date: 2022-09-11 12:44:50.504839

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5381b0430501'
down_revision = 'fef59b19ba06'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")))
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
