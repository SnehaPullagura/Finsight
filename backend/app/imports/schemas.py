from typing import List, Dict, Optional, Any
from pydantic import BaseModel

class ImportPreviewItem(BaseModel):
    date: str
    description: str
    amount: float
    type: str # "income" or "expense"
    suggested_category: str
    merchant: str
    is_duplicate: bool

class ImportJobResponse(BaseModel):
    job_id: str
    filename: str
    status: str # "completed", "failed"
    total_records: int
    imported_records: int
    duplicate_records: int
    preview: List[ImportPreviewItem]
