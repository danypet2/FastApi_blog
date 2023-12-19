"""Update model post

Revision ID: 500b1fcee3f1
Revises: 29cf05bfa75a
Create Date: 2023-12-19 18:50:29.057531

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '500b1fcee3f1'
down_revision: Union[str, None] = '29cf05bfa75a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=40), nullable=True),
    sa.Column('content', sa.String(length=10000), nullable=True),
    sa.Column('image', sa.String(length=1000), nullable=True),
    sa.Column('data_published', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('data_updated', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_id'), 'post', ['id'], unique=False)
    op.drop_index('ix_posts_id', table_name='posts')
    op.drop_table('posts')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=40), autoincrement=False, nullable=True),
    sa.Column('content', sa.VARCHAR(length=10000), autoincrement=False, nullable=True),
    sa.Column('image', sa.VARCHAR(length=1000), autoincrement=False, nullable=True),
    sa.Column('data_published', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('data_updated', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='posts_pkey')
    )
    op.create_index('ix_posts_id', 'posts', ['id'], unique=False)
    op.drop_index(op.f('ix_post_id'), table_name='post')
    op.drop_table('post')
    # ### end Alembic commands ###
