import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from backend.app.goals.models import GoalType, GoalStatus

class GoalCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=128)
    goal_type: GoalType = GoalType.CUSTOM
    target_amount: float = Field(..., gt=0)
    current_amount: float = Field(default=0.0, ge=0)
    target_date: datetime.date
    monthly_contribution: float = Field(default=0.0, ge=0)
    account_id: Optional[int] = None
    notes: Optional[str] = None

class GoalUpdate(BaseModel):
    name: Optional[str] = None
    target_amount: Optional[float] = None
    current_amount: Optional[float] = None
    target_date: Optional[datetime.date] = None
    monthly_contribution: Optional[float] = None
    status: Optional[GoalStatus] = None
    notes: Optional[str] = None

class GoalContributionCreate(BaseModel):
    amount: float = Field(..., gt=0)
    contribution_date: Optional[datetime.date] = None
    notes: Optional[str] = None

class GoalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    name: str
    goal_type: GoalType
    target_amount: float
    current_amount: float
    target_date: datetime.date
    monthly_contribution: float
    status: GoalStatus
    percentage_completed: float
    projected_completion_date: Optional[datetime.date] = None
    sufficiency_status: str # "on_track", "behind", "ahead"
    notes: Optional[str] = None
    created_at: datetime.datetime
