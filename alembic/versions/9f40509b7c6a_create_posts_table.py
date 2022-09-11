"""create posts table

Revision ID: 9f40509b7c6a
Revises: 
Create Date: 2022-09-10 17:59:38.577750

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f40509b7c6a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column("id", sa.Integer(), nullable=False, primary_key=True), sa.Column("title", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
