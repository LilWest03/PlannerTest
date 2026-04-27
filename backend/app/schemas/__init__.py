from app.schemas.auth import AuthResponse, AuthUser, LoginRequest, RegisterRequest
from app.schemas.activity import ActivityLogItem
from app.schemas.document import DocumentCreateRequest, DocumentItem, DocumentUploadResponse
from app.schemas.run_history import AgentRunItem, SchedulerRunItem
from app.schemas.task import TaskCreateRequest, TaskItem, TaskSummary, TaskUpdateRequest
from app.schemas.workspace import (
    WorkspaceCreateRequest,
    WorkspaceHighlight,
    WorkspaceItem,
    WorkspaceOverview,
    WorkspaceStats,
    WorkspaceTask,
)
