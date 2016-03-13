"""add stock_account table

Revision ID: af47dfaccf2
Revises: 1ab44c4cbc99
Create Date: 2016-03-12 20:16:09.322739

"""

# revision identifiers, used by Alembic.
revision = 'af47dfaccf2'
down_revision = '1ab44c4cbc99'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stock_account',
    sa.Column('trading_date', sa.Date(), nullable=False),
    sa.Column('personal_new', sa.Float(), nullable=True),
    sa.Column('company_new', sa.Float(), nullable=True),
    sa.Column('personal_total_a', sa.Float(), nullable=True),
    sa.Column('personal_total_b', sa.Float(), nullable=True),
    sa.Column('company_total_a', sa.Float(), nullable=True),
    sa.Column('company_total_b', sa.Float(), nullable=True),
    sa.Column('position_a', sa.Float(), nullable=True),
    sa.Column('position_b', sa.Float(), nullable=True),
    sa.Column('trading_a', sa.Float(), nullable=True),
    sa.Column('trading_b', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('trading_date'),
    sa.UniqueConstraint('trading_date')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stock_account')
    ### end Alembic commands ###