from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from backend.app.categories.models import CategoryGroup

class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=64)
    group: CategoryGroup
    icon: Optional[str] = "Tag"
    color: Optional[str] = "#6366F1"
    is_tax_deductible: bool = False

class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str
    group: CategoryGroup
    icon: str
    color: str
    is_tax_deductible: bool
    is_system_default: bool
