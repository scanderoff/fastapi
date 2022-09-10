"""add user table

Revision ID: ef3558c3588f
Revises: 11459f6d2636
Create Date: 2022-09-02 23:28:26.355303

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef3558c3588f'
down_revision = '11459f6d2636'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  server_default=sa.text('NOW()'), nullable=False),
        sa.PrimaryKeyConstraint('id'), # второй способ создания primary key
        sa.UniqueConstraint('email'),
    )


def downgrade() -> None:
    op.drop_table('user')
