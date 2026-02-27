"""rename project statuses

Revision ID: c2d3e4f5a6b7
Revises: b1c2d3e4f5a6
Create Date: 2026-02-27 00:01:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2d3e4f5a6b7'
down_revision = 'b1c2d3e4f5a6'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("UPDATE projects SET status = 'in_development' WHERE status = 'in_progress'")
    op.execute("UPDATE projects SET status = 'live' WHERE status = 'complete'")


def downgrade():
    op.execute("UPDATE projects SET status = 'in_progress' WHERE status = 'in_development'")
    op.execute("UPDATE projects SET status = 'complete' WHERE status = 'live'")
