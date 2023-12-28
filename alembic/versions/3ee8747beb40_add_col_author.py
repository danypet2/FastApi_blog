"""add col author

Revision ID: 3ee8747beb40
Revises: 4f8606dea4c8
Create Date: 2023-12-25 18:15:54.882111

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ee8747beb40'
down_revision: Union[str, None] = '4f8606dea4c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('author_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'post', 'user', ['author_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_column('post', 'author_id')
    # ### end Alembic commands ###
