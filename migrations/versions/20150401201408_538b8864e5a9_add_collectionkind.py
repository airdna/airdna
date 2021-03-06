"""Add CollectionKind.

Revision ID: 538b8864e5a9
Revises: 458dc7cf9150
Create Date: 2015-04-01 20:14:08.086792

"""

# revision identifiers, used by Alembic.
revision = '538b8864e5a9'
down_revision = '458dc7cf9150'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('collection_kind',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column(u'collection', sa.Column('kind_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'collection', 'collection_kind', ['kind_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'collection', type_='foreignkey')
    op.drop_column(u'collection', 'kind_id')
    op.drop_table('collection_kind')
    ### end Alembic commands ###
