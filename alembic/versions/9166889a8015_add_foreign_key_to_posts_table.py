"""add foreign-key to posts table

Revision ID: 9166889a8015
Revises: 1e186aec8ed7
Create Date: 2021-11-16 00:02:23.775830

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9166889a8015'
down_revision = '1e186aec8ed7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users',
    local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
