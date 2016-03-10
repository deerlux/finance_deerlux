"""add the default country for moneydata

Revision ID: 2331e3fe577
Revises: 3be30b3e829
Create Date: 2015-12-07 22:54:50.605315

"""

# revision identifiers, used by Alembic.
revision = '2331e3fe577'
down_revision = '3be30b3e829'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('money_data', 'country_id', 
            server_default='1')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('money_data', 'country_id',
            server_default = None)
    ### end Alembic commands ###
