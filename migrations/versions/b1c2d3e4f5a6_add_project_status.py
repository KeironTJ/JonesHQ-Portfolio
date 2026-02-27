"""add project status

Revision ID: b1c2d3e4f5a6
Revises: a04b4a959155
Create Date: 2026-02-27 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1c2d3e4f5a6'
down_revision = 'a04b4a959155'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.add_column(sa.Column(
            'status', sa.String(length=32), nullable=False,
            server_default='in_progress'
        ))


def downgrade():
    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.drop_column('status')
