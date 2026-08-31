from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.auth.dependencies import get_current_user
from backend.app.auth.models import User
from backend.app.reports.schemas import ReportGenerateRequest, ReportGenerateResponse
from backend.app.reports.service import ReportGeneratorService

router = APIRouter(prefix="/reports", tags=["Reports Generator"])

@router.post("/generate", response_model=ReportGenerateResponse)
async def generate_report(
    req: ReportGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await ReportGeneratorService.generate_report(db, current_user.id, req)

@router.get("/download/{report_id}")
async def download_report(report_id: str):
    csv_content = "Date,Description,Merchant,Amount,Type,Category\n"
    csv_content += f"{datetime.date.today()},Sample Salary,Employer,85000,income,Salary & Wages\n"
    csv_content += f"{datetime.date.today()},Swiggy Instamart,Instamart,1240,expense,Groceries & Supermarket\n"
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=finsight_report_{report_id}.csv"}
    )
