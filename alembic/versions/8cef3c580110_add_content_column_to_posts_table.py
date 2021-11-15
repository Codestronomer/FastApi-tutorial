"""add content column to posts table

Revision ID: 8cef3c580110
Revises: 3a5c7160fd62
Create Date: 2021-11-15 23:43:51.733462

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8cef3c580110'
down_revision = '3a5c7160fd62'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass

def downgrade():
    op.drop_column('posts', 'content')
