"""add contact_email and skills_heading to site_settings

Revision ID: f6a7b8c9d0e1
Revises: e5f6a7b8c9d0
Create Date: 2026-03-03 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'f6a7b8c9d0e1'
down_revision = 'e5f6a7b8c9d0'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('site_settings', schema=None) as batch_op:
        batch_op.add_column(sa.Column('contact_email', sa.String(length=256), nullable=True))
        batch_op.add_column(sa.Column('skills_heading', sa.String(length=128), nullable=True,
                                      server_default='Skills'))


def downgrade():
    with op.batch_alter_table('site_settings', schema=None) as batch_op:
        batch_op.drop_column('skills_heading')
        batch_op.drop_column('contact_email')
