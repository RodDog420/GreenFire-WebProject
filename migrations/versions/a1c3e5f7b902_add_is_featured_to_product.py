"""add is_featured to product

Revision ID: a1c3e5f7b902
Revises: 6b855672deed
Create Date: 2026-04-18

"""
from alembic import op
import sqlalchemy as sa

revision = 'a1c3e5f7b902'
down_revision = '6b855672deed'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'products',
        sa.Column(
            'is_featured',
            sa.Boolean(),
            nullable=False,
            server_default='false',
        )
    )


def downgrade():
    op.drop_column('products', 'is_featured')
