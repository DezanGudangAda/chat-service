"""reconfig migrations

Revision ID: d8274b4470e8
Revises: 
Create Date: 2022-04-27 11:50:04.417524

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8274b4470e8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('base_question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question', sa.String(), nullable=True),
    sa.Column('is_automate_reply', sa.Boolean(), nullable=True),
    sa.Column('context', sa.String(), nullable=True),
    sa.Column('code', sa.String(), nullable=True),
    sa.Column('trigger_action', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_base_question_id'), 'base_question', ['id'], unique=False)
    op.create_table('channel',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('buyer_getstream_id', sa.String(), nullable=True),
    sa.Column('seller_getstream_id', sa.String(), nullable=True),
    sa.Column('channel_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_channel_channel_name'), 'channel', ['channel_name'], unique=False)
    op.create_index(op.f('ix_channel_id'), 'channel', ['id'], unique=False)
    op.create_table('qna_journey',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('path', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('related_answer',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('answer', sa.String(), nullable=True),
    sa.Column('trigger_action', sa.String(), nullable=True),
    sa.Column('code', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('related_question',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('question', sa.String(), nullable=True),
    sa.Column('is_automate_reply', sa.Boolean(), nullable=True),
    sa.Column('trigger_action', sa.String(), nullable=True),
    sa.Column('context', sa.String(), nullable=True),
    sa.Column('code', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('stream_token', sa.String(), nullable=True),
    sa.Column('account_type', sa.String(), nullable=False),
    sa.Column('getstream_id', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('related_question')
    op.drop_table('related_answer')
    op.drop_table('qna_journey')
    op.drop_index(op.f('ix_channel_id'), table_name='channel')
    op.drop_index(op.f('ix_channel_channel_name'), table_name='channel')
    op.drop_table('channel')
    op.drop_index(op.f('ix_base_question_id'), table_name='base_question')
    op.drop_table('base_question')
    # ### end Alembic commands ###