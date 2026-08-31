from typing import Any, Dict, List, Tuple
from pydantic import BaseModel

class DAGExecutionRequest(BaseModel):
    nodes: Dict[str, Dict[str, Any]]
    edges: List[Tuple[str, str]]
    initial_context: Dict[str, Any]

class ExpressionEvalRequest(BaseModel):
    expression: str
    context: Dict[str, Any]

class DSRExportRequest(BaseModel):
    subject_email: str
