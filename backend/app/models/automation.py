import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.models.base import Base, UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin

class AutomationWorkflow(UUIDModel, TimestampMixin, SoftDeleteMixin, TenantMixin):
    __tablename__ = "automation_workflows"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Optional[Mapped[str]] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    trigger_event: Mapped[str] = mapped_column(String(100), nullable=False, index=True) # deal.stage_changed, lead.created, lead.score_threshold, task.due, contact.created
    trigger_config: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    conditions: Mapped[List["WorkflowCondition"]] = relationship("WorkflowCondition", back_populates="workflow", cascade="all, delete-orphan")
    actions: Mapped[List["WorkflowAction"]] = relationship("WorkflowAction", back_populates="workflow", cascade="all, delete-orphan", order_by="WorkflowAction.execution_order.asc()")
    execution_logs: Mapped[List["WorkflowExecutionLog"]] = relationship("WorkflowExecutionLog", back_populates="workflow", cascade="all, delete-orphan")

class WorkflowCondition(UUIDModel):
    __tablename__ = "workflow_conditions"

    workflow_id: Mapped[str] = mapped_column(String(36), ForeignKey("automation_workflows.id", ondelete="CASCADE"), nullable=False, index=True)
    field_path: Mapped[str] = mapped_column(String(100), nullable=False) # e.g. value, score, lifecycle_stage
    operator: Mapped[str] = mapped_column(String(20), nullable=False) # gt, gte, lt, lte, eq, neq, contains, in
    target_value: Mapped[str] = mapped_column(String(255), nullable=False)

    workflow: Mapped["AutomationWorkflow"] = relationship("AutomationWorkflow", back_populates="conditions")

class WorkflowAction(UUIDModel):
    __tablename__ = "workflow_actions"

    workflow_id: Mapped[str] = mapped_column(String(36), ForeignKey("automation_workflows.id", ondelete="CASCADE"), nullable=False, index=True)
    action_type: Mapped[str] = mapped_column(String(50), nullable=False) # send_email, create_task, update_field, reassign_owner, trigger_webhook, request_approval
    action_config: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    execution_order: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    workflow: Mapped["AutomationWorkflow"] = relationship("AutomationWorkflow", back_populates="actions")

class WorkflowExecutionLog(UUIDModel, TimestampMixin, TenantMixin):
    __tablename__ = "workflow_execution_logs"

    workflow_id: Mapped[str] = mapped_column(String(36), ForeignKey("automation_workflows.id", ondelete="CASCADE"), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(36), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False) # success, failed, skipped
    error_message: Optional[Mapped[str]] = mapped_column(Text, nullable=True)
    payload_snapshot: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    workflow: Mapped["AutomationWorkflow"] = relationship("AutomationWorkflow", back_populates="execution_logs")
