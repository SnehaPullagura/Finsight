import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, ConfigDict
from backend.app.auth.schemas import UserPublicResponse

class ModelRegistryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    model_name: str
    version: str
    algorithm: str
    accuracy_or_metric: float
    training_sample_count: int
    is_active: bool
    created_at: datetime.datetime

class PlatformMetricsResponse(BaseModel):
    total_users: int
    active_users_30d: int
    total_transactions_managed: int
    total_accounts_connected: int
    total_volume_processed: float
    system_health_status: str
    active_ml_models: List[ModelRegistryResponse]
