from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Workspace(TimestampMixin, Base):
    __tablename__ = "workspaces"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    owner_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    focus_mode: Mapped[str] = mapped_column(String(40), nullable=False, default="balanced")
    scheduler_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    reminder_window_hours: Mapped[int] = mapped_column(Integer, nullable=False, default=24)
    max_tasks_per_run: Mapped[int] = mapped_column(Integer, nullable=False, default=2)

    owner = relationship("User", back_populates="workspaces")
    tasks = relationship("Task", back_populates="workspace", cascade="all, delete-orphan")
    activity_logs = relationship("ActivityLog", back_populates="workspace", cascade="all, delete-orphan")
    scheduler_runs = relationship("SchedulerRun", back_populates="workspace", cascade="all, delete-orphan")
    agent_runs = relationship("AgentRun", back_populates="workspace", cascade="all, delete-orphan")
