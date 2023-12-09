"""Initial Migration

Revision ID: 79a957ad1c40
Revises: 
Create Date: 2023-12-09 00:06:32.681828

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79a957ad1c40'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('punches', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_and_time', sa.DateTime(), nullable=True))

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fav_color', sa.String(length=120), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('fav_color')

    with op.batch_alter_table('punches', schema=None) as batch_op:
        batch_op.drop_column('date_and_time')

    # ### end Alembic commands ###