"""chang stock.stock_name column len

Revision ID: 1ab44c4cbc99
Revises: 2331e3fe577
Create Date: 2015-12-10 17:35:24.020714

"""

# revision identifiers, used by Alembic.
revision = '1ab44c4cbc99'
down_revision = '2331e3fe577'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('stock','stock_name',type_=sa.String(32))

def downgrade():
    op.alter_column('stock','stock_name',type_=sa.String(16))

