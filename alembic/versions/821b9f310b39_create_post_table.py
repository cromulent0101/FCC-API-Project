"""Create post table

Revision ID: 821b9f310b39
Revises: 
Create Date: 2021-11-30 18:25:08.642799

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '821b9f310b39'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',sa.Column('id',sa.Integer,nullable=False,primary_key=True),
        sa.Column('title',sa.String,nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
