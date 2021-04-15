"""empty message

Revision ID: 72048727bac4
Revises: 52b2d27c8435
Create Date: 2021-04-12 16:54:34.537645

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72048727bac4'
down_revision = '52b2d27c8435'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('picture', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('picture')

    # ### end Alembic commands ###