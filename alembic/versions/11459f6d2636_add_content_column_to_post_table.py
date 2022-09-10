"""add content column to post table

Revision ID: 11459f6d2636
Revises: ecbc91facc3d
Create Date: 2022-09-02 23:21:59.128793

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11459f6d2636'
down_revision = 'ecbc91facc3d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'post',
        sa.Column('content', sa.String(), nullable=False),
    )


def downgrade() -> None:
    op.drop_column('post', 'content')
