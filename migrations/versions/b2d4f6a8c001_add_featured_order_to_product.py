"""add featured_order to product

Revision ID: b2d4f6a8c001
Revises: a1c3e5f7b902
Create Date: 2026-04-18

"""
from alembic import op
import sqlalchemy as sa

revision = 'b2d4f6a8c001'
down_revision = 'a1c3e5f7b902'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'products',
        sa.Column('featured_order', sa.Integer(), nullable=True)
    )


def downgrade():
    op.drop_column('products', 'featured_order')
