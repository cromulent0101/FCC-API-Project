"""Add foreign key to posts table

Revision ID: da6e93e1c51c
Revises: 1495d88a5411
Create Date: 2021-11-30 18:53:51.966508

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da6e93e1c51c'
down_revision = '1495d88a5411'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('owner_id',sa.Integer,nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users',
                            local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass



def downgrade():
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
