"""add content column to posts table

Revision ID: 8cd5693938b2
Revises: 9f40509b7c6a
Create Date: 2022-09-11 00:45:36.669353

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8cd5693938b2'
down_revision = '9f40509b7c6a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
