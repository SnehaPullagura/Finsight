from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.session import get_db
from backend.app.auth.dependencies import get_current_user
from backend.app.auth.models import User
from backend.app.scenarios.schemas import ScenarioCreate, ScenarioResponse, ScenarioComparisonMatrix
from backend.app.scenarios.service import ScenarioSimulationEngine

router = APIRouter(prefix="/scenarios", tags=["What-If Scenario Simulator"])

@router.post("", response_model=ScenarioResponse, status_code=status.HTTP_201_CREATED)
async def create_and_simulate_scenario(
    data: ScenarioCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await ScenarioSimulationEngine.simulate_scenario(db, current_user.id, data)

@router.get("/compare", response_model=ScenarioComparisonMatrix)
async def compare_scenarios(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await ScenarioSimulationEngine.get_comparison_matrix(db, current_user.id)
