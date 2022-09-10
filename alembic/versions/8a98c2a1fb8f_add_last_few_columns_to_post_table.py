"""add last few columns to post table

Revision ID: 8a98c2a1fb8f
Revises: 1275abf9f681
Create Date: 2022-09-02 23:44:06.759340

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a98c2a1fb8f'
down_revision = '1275abf9f681'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'post',
        sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),
    )

    op.add_column(
        'post',
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),
    )


def downgrade() -> None:
    op.drop_column('post', 'published')
    op.drop_column('post', 'created_at')
