"""add foreign key to post table

Revision ID: 1275abf9f681
Revises: ef3558c3588f
Create Date: 2022-09-02 23:37:39.884791

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1275abf9f681'
down_revision = 'ef3558c3588f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'post',
        sa.Column('owner_id', sa.Integer(), nullable=False),
    )

    op.create_foreign_key(
        'post_user_fk',
        source_table='post',
        referent_table='user',
        local_cols=('owner_id',),
        remote_cols=('id',),
        ondelete='CASCADE',
    )


def downgrade() -> None:
    op.drop_constraint('post_user_fk', table_name='post')
    op.drop_column('post', 'owner_id')
