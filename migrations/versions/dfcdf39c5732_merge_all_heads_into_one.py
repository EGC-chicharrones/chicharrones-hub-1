"""Merge all heads into one

Revision ID: dfcdf39c5732
Revises: 1cf2dd42552a, 2173bfe555cb, 6d79e74ed343
Create Date: 2024-12-15 10:11:39.312204

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dfcdf39c5732'
down_revision = ('1cf2dd42552a', '2173bfe555cb', '6d79e74ed343')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
