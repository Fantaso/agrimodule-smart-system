"""empty message

Revision ID: 3c32128bf8b0
Revises: 29cb5274edf0
Create Date: 2018-06-21 19:14:57.522832

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c32128bf8b0'
down_revision = '29cb5274edf0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('welcome',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('add_agrisys', sa.Boolean(), nullable=True),
    sa.Column('install_agrisys', sa.Boolean(), nullable=True),
    sa.Column('add_pump', sa.Boolean(), nullable=True),
    sa.Column('add_farm', sa.Boolean(), nullable=True),
    sa.Column('add_field', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('welcome')
    # ### end Alembic commands ###