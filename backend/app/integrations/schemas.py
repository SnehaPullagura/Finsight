from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class ConnectionCreateRequest(BaseModel):
    provider: str
    name: str
    auth_type: str = "api_key"
    credentials: Dict[str, Any]
    settings: Optional[Dict[str, Any]] = None

class ConnectionResponse(BaseModel):
    id: str
    provider: str
    name: str
    status: str
    auth_type: str
    is_active: bool

class MigrationPreviewRequest(BaseModel):
    csv_content: str
    field_mappings: Dict[str, str]

class MigrationPreviewResponse(BaseModel):
    total_parsed: int
    valid_count: int
    rejected_count: int
    sample_valid: List[Dict[str, str]]
    sample_rejected: List[Dict[str, Any]]
