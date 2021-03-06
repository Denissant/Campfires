"""empty message

Revision ID: 2a3e4d065793
Revises: 
Create Date: 2021-04-22 18:45:20.078784

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a3e4d065793'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=16), nullable=False),
    sa.Column('name_first', sa.String(), nullable=True),
    sa.Column('name_last', sa.String(), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('sex', sa.String(), nullable=True),
    sa.Column('dob', sa.Date(), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('picture', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users'))
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_users_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_users_username'), ['username'], unique=True)

    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('media', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_posts_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_posts'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_username'))
        batch_op.drop_index(batch_op.f('ix_users_email'))

    op.drop_table('users')
    # ### end Alembic commands ###
