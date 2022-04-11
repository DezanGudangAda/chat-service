"""initial db

Revision ID: cdacce5864f8
Revises: 
Create Date: 2022-04-11 10:13:36.596599

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cdacce5864f8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('answer',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('answer', sa.String(), nullable=True),
    sa.Column('question_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question', sa.String(), nullable=True),
    sa.Column('is_automate_reply', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_question_id'), 'question', ['id'], unique=False)
    op.create_table('room',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('buyer_id', sa.String(), nullable=True),
    sa.Column('seller_id', sa.String(), nullable=True),
    sa.Column('channel_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('stream_token', sa.String(), nullable=True),
    sa.Column('account_type', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('room')
    op.drop_index(op.f('ix_question_id'), table_name='question')
    op.drop_table('question')
    op.drop_table('answer')
    # ### end Alembic commands ###
