"""empty message

Revision ID: 1cf6e228f40b
Revises: 3da9f0048412
Create Date: 2015-07-23 20:20:09.742193

"""

# revision identifiers, used by Alembic.
revision = '1cf6e228f40b'
down_revision = '3da9f0048412'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('published_count', sa.Integer(), nullable=False, default = 0))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'published_count')
    ### end Alembic commands ###