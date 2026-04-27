"""add workspace scheduler settings

Revision ID: 20260427_0005
Revises: 20260427_0004
Create Date: 2026-04-27 00:30:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260427_0005"
down_revision = "20260427_0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "workspaces",
        sa.Column("scheduler_enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.add_column(
        "workspaces",
        sa.Column("reminder_window_hours", sa.Integer(), nullable=False, server_default=sa.text("24")),
    )
    op.add_column(
        "workspaces",
        sa.Column("max_tasks_per_run", sa.Integer(), nullable=False, server_default=sa.text("2")),
    )
    op.alter_column("workspaces", "scheduler_enabled", server_default=None)
    op.alter_column("workspaces", "reminder_window_hours", server_default=None)
    op.alter_column("workspaces", "max_tasks_per_run", server_default=None)


def downgrade() -> None:
    op.drop_column("workspaces", "max_tasks_per_run")
    op.drop_column("workspaces", "reminder_window_hours")
    op.drop_column("workspaces", "scheduler_enabled")
