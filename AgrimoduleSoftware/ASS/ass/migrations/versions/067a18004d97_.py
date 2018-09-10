"""empty message

Revision ID: 067a18004d97
Revises: 35dcc9d63d72
Create Date: 2018-06-21 15:36:49.299570

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '067a18004d97'
down_revision = '35dcc9d63d72'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('agrimodulelist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('identifier', sa.String(length=100), nullable=False),
    sa.Column('type', sa.String(length=10), nullable=False),
    sa.Column('has_user_registered', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('has_agrimodule_registered', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('identifier')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('agrimodulelist')
    # ### end Alembic commands ###