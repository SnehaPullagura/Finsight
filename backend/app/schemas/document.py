from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class DocumentFolderCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    parent_id: Optional[str] = None

class DocumentFolderResponse(BaseModel):
    id: str
    name: str
    parent_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class DocumentResponse(BaseModel):
    id: str
    tenant_id: str
    name: str
    file_size_bytes: int
    mime_type: str
    folder_id: Optional[str] = None
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    uploaded_by_id: Optional[str] = None
    is_public: bool
    download_count: int
    tags: List[str] = []
    created_at: datetime

    class Config:
        from_attributes = True
