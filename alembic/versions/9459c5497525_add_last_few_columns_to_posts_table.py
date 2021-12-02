"""Add last few columns to posts table

Revision ID: 9459c5497525
Revises: da6e93e1c51c
Create Date: 2021-12-01 19:17:44.647011

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9459c5497525'
down_revision = 'da6e93e1c51c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published',sa.Boolean(),nullable=False,server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at',sa.TIMESTAMP(timezone=True), nullable = False, server_default = sa.text('now()'))) # use default instead of server_default
    pass


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass

