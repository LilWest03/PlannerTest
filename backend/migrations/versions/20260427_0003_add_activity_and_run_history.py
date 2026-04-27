"""add activity log and run history tables

Revision ID: 20260427_0003
Revises: 20260426_0002
Create Date: 2026-04-27 00:30:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260427_0003"
down_revision = "20260426_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "activity_logs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("workspace_id", sa.String(length=36), nullable=False),
        sa.Column("actor_user_id", sa.String(length=36), nullable=False),
        sa.Column("category", sa.String(length=40), nullable=False),
        sa.Column("action", sa.String(length=80), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("entity_type", sa.String(length=40), nullable=True),
        sa.Column("entity_id", sa.String(length=36), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["actor_user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_activity_logs_actor_user_id"), "activity_logs", ["actor_user_id"], unique=False)
    op.create_index(op.f("ix_activity_logs_workspace_id"), "activity_logs", ["workspace_id"], unique=False)

    op.create_table(
        "scheduler_runs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("workspace_id", sa.String(length=36), nullable=False),
        sa.Column("owner_id", sa.String(length=36), nullable=False),
        sa.Column("job_name", sa.String(length=80), nullable=False),
        sa.Column("trigger_type", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_scheduler_runs_owner_id"), "scheduler_runs", ["owner_id"], unique=False)
    op.create_index(op.f("ix_scheduler_runs_workspace_id"), "scheduler_runs", ["workspace_id"], unique=False)

    op.create_table(
        "agent_runs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("scheduler_run_id", sa.String(length=36), nullable=True),
        sa.Column("workspace_id", sa.String(length=36), nullable=False),
        sa.Column("owner_id", sa.String(length=36), nullable=False),
        sa.Column("agent_key", sa.String(length=60), nullable=False),
        sa.Column("agent_name", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("target_type", sa.String(length=40), nullable=True),
        sa.Column("target_id", sa.String(length=36), nullable=True),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("output_summary", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["scheduler_run_id"], ["scheduler_runs.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_agent_runs_owner_id"), "agent_runs", ["owner_id"], unique=False)
    op.create_index(op.f("ix_agent_runs_scheduler_run_id"), "agent_runs", ["scheduler_run_id"], unique=False)
    op.create_index(op.f("ix_agent_runs_workspace_id"), "agent_runs", ["workspace_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_agent_runs_workspace_id"), table_name="agent_runs")
    op.drop_index(op.f("ix_agent_runs_scheduler_run_id"), table_name="agent_runs")
    op.drop_index(op.f("ix_agent_runs_owner_id"), table_name="agent_runs")
    op.drop_table("agent_runs")
    op.drop_index(op.f("ix_scheduler_runs_workspace_id"), table_name="scheduler_runs")
    op.drop_index(op.f("ix_scheduler_runs_owner_id"), table_name="scheduler_runs")
    op.drop_table("scheduler_runs")
    op.drop_index(op.f("ix_activity_logs_workspace_id"), table_name="activity_logs")
    op.drop_index(op.f("ix_activity_logs_actor_user_id"), table_name="activity_logs")
    op.drop_table("activity_logs")
