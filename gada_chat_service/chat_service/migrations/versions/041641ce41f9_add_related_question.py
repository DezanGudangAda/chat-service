"""add related question

Revision ID: 041641ce41f9
Revises: df0d5fcc3094
Create Date: 2022-04-14 10:26:46.928336

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '041641ce41f9'
down_revision = 'df0d5fcc3094'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('related_answer',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('answer', sa.String(), nullable=True),
    sa.Column('id_base_question', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('related_question',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_related_answer', sa.Integer(), nullable=True),
    sa.Column('question', sa.String(), nullable=True),
    sa.Column('is_automate_reply', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('related_question')
    op.drop_table('related_answer')
    # ### end Alembic commands ###
