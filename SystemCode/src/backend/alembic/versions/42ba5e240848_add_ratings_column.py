"""Add ratings column

Revision ID: 42ba5e240848
Revises: 082466f7d07d
Create Date: 2023-05-03 08:11:58.533960

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '42ba5e240848'
down_revision = '082466f7d07d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('results', sa.Column('user_rating', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('results', 'user_rating')
    # ### end Alembic commands ###
