"""Add user table

Revision ID: 1495d88a5411
Revises: 3b3e70718485
Create Date: 2021-11-30 18:38:57.449825

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1495d88a5411'
down_revision = '3b3e70718485'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id',sa.Integer,nullable=False,primary_key=True),
                    sa.Column('email',sa.String,nullable=False),
                    sa.Column('password',sa.String,nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                                                        server_default=sa.text('now()'),nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
