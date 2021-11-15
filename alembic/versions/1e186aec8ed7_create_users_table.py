"""create users table

Revision ID: 1e186aec8ed7
Revises: 8cef3c580110
Create Date: 2021-11-15 23:49:28.327531

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e186aec8ed7'
down_revision = '8cef3c580110'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users', 
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String, nullable=False),
        sa.Column('username', sa.String, nullable=False),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('created', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.UniqueConstraint('email', 'username'),
        sa.PrimaryKeyConstraint('id')
        )
    pass


def downgrade():
    pass
