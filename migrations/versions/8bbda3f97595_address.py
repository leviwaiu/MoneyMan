"""Address

Revision ID: 8bbda3f97595
Revises: f2adb480b915
Create Date: 2018-11-18 06:59:09.057730

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8bbda3f97595'
down_revision = 'f2adb480b915'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('city', sa.String(length=128), nullable=True))
    op.add_column('user', sa.Column('state', sa.String(length=128), nullable=True))
    op.add_column('user', sa.Column('street', sa.String(length=128), nullable=True))
    op.add_column('user', sa.Column('streetNo', sa.String(length=128), nullable=True))
    op.add_column('user', sa.Column('zipcode', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'zipcode')
    op.drop_column('user', 'streetNo')
    op.drop_column('user', 'street')
    op.drop_column('user', 'state')
    op.drop_column('user', 'city')
    # ### end Alembic commands ###