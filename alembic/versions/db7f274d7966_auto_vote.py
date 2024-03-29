"""auto-vote

Revision ID: db7f274d7966
Revises: 9459c5497525
Create Date: 2021-12-01 19:41:45.746495

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db7f274d7966'
down_revision = '9459c5497525'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('user_id',sa.Integer(),nullable=False),
    sa.Column('post_id',sa.Integer(),nullable=False),
    sa.ForeignKeyConstraint(['post_id'],['posts.id'],ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'],['users.id'],ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id','post_id')
    )


    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votes')
    # ### end Alembic commands ###
