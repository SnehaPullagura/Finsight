from typing import Dict, List, Optional, Any
from pydantic import BaseModel

class SearchResultItem(BaseModel):
    id: str
    entity_type: str # contact, company, lead, deal, task, document, ticket
    title: str
    subtitle: Optional[str] = None
    url: str
    highlights: List[str] = []
    metadata: Dict[str, Any] = {}

class GlobalSearchResponse(BaseModel):
    query: str
    total_results: int
    results_by_type: Dict[str, List[SearchResultItem]]
    results: List[SearchResultItem]
