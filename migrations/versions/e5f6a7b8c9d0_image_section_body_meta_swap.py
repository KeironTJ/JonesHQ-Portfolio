"""image section: swap body (url) and meta (caption) so body holds text

Revision ID: e5f6a7b8c9d0
Revises: d3e4f5a6b7c8
Create Date: 2026-02-27 12:00:00.000000

body was repurposed as the image URL for image sections, leaving nowhere for
descriptive text. This migration swaps them: meta stores the URL/path and
body stores optional accompanying text (matching all other section types).
"""
from alembic import op

revision = 'e5f6a7b8c9d0'
down_revision = 'd3e4f5a6b7c8'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        UPDATE project_sections
        SET body = COALESCE(meta, ''),
            meta = body
        WHERE section_type = 'image'
    """)


def downgrade():
    op.execute("""
        UPDATE project_sections
        SET body = COALESCE(meta, ''),
            meta = body
        WHERE section_type = 'image'
    """)
