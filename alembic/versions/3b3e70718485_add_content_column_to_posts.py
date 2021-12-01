"""Add content column to posts

Revision ID: 3b3e70718485
Revises: 821b9f310b39
Create Date: 2021-11-30 18:34:34.553321

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b3e70718485'
down_revision = '821b9f310b39'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content',sa.String,nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
