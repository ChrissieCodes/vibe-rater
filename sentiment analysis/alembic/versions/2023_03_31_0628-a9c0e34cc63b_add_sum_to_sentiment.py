"""add sum to sentiment

Revision ID: a9c0e34cc63b
Revises: 4e555a6b7a90
Create Date: 2023-03-31 06:28:57.996454

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm


# revision identifiers, used by Alembic.
revision = 'a9c0e34cc63b'
down_revision = '4e555a6b7a90'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('sentiment',sa.Column('vibe_sum',sa.Float(3),nullable=True))

    


def downgrade() -> None:
    op.drop_column('sentiment','vibe_sum')
