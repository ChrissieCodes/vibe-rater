"""create_sentiment_table

Revision ID: 4e555a6b7a90
Revises: 
Create Date: 2022-12-08 00:14:46.078381

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e555a6b7a90'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'sentiment',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username',sa.String(50), nullable = True),
        sa.Column('positive',sa.Float(3),nullable =True),
        sa.Column('neutral',sa.Float(3),nullable =True),
        sa.Column('negative',sa.Float(3),nullable =True),
        sa.Column('number_of_chats',sa.Integer, nullable = True),


        
    )


def downgrade():
    op.drop_table('sentiment')

