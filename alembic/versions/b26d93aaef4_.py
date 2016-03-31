"""empty message

Revision ID: b26d93aaef4
Revises: af47dfaccf2
Create Date: 2016-03-23 22:19:30.148959

"""

# revision identifiers, used by Alembic.
revision = 'b26d93aaef4'
down_revision = 'af47dfaccf2'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stock_new',
    sa.Column('stock_code', sa.String(length=12), nullable=False),
    sa.Column('stock_name', sa.String(length=32), nullable=False),
    sa.Column('market', sa.String(length=8), nullable=True),
    sa.PrimaryKeyConstraint('stock_code')
    )
    op.create_unique_constraint(None, 'stock_account', ['trading_date'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'stock_account', type_='unique')
    op.drop_table('stock_new')
    ### end Alembic commands ###