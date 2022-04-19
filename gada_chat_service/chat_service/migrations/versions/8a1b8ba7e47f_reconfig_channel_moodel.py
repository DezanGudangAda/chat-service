"""reconfig channel moodel

Revision ID: 8a1b8ba7e47f
Revises: be68c1494ea8
Create Date: 2022-04-12 10:15:54.341105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a1b8ba7e47f'
down_revision = 'be68c1494ea8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('channel', sa.Column('buyer_getstream_id', sa.String(), nullable=True))
    op.add_column('channel', sa.Column('seller_getstream_id', sa.String(), nullable=True))
    op.drop_column('channel', 'buyer_id')
    op.drop_column('channel', 'seller_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('channel', sa.Column('seller_id', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('channel', sa.Column('buyer_id', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('channel', 'seller_getstream_id')
    op.drop_column('channel', 'buyer_getstream_id')
    # ### end Alembic commands ###