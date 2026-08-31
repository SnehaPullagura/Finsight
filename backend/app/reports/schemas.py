from typing import List, Dict, Optional
from pydantic import BaseModel

class ReportGenerateRequest(BaseModel):
    report_type: str = "monthly_summary" # monthly_summary, annual_tax, cash_flow, health_audit
    format: str = "csv" # csv, excel, pdf
    month: Optional[int] = None
    year: Optional[int] = None

class ReportGenerateResponse(BaseModel):
    report_id: str
    report_name: str
    format: str
    download_url: str
    generated_at: str
    summary_metrics: Dict[str, float]
