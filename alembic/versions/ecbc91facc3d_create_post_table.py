"""create post table

Revision ID: ecbc91facc3d
Revises: 
Create Date: 2022-09-02 23:11:18.332826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ecbc91facc3d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'post',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('post')
