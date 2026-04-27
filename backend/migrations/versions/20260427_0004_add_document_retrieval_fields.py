"""add document retrieval fields

Revision ID: 20260427_0004
Revises: 20260427_0003
Create Date: 2026-04-27 01:30:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260427_0004"
down_revision = "20260427_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("documents", sa.Column("extracted_text", sa.Text(), nullable=True))
    op.add_column("documents", sa.Column("retrieval_preview", sa.Text(), nullable=True))
    op.add_column("documents", sa.Column("indexed_at", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column("documents", "indexed_at")
    op.drop_column("documents", "retrieval_preview")
    op.drop_column("documents", "extracted_text")
