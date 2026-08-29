from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.customer_success import CustomerSuccessPlan, OnboardingMilestone
from backend.app.models.support import Ticket
from backend.app.repositories.customer_success import SuccessPlanRepository
from backend.app.services.base import BaseService
from backend.app.schemas.customer_success import SuccessPlanCreate, MilestoneCreate

class CustomerSuccessService(BaseService[CustomerSuccessPlan, SuccessPlanRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(SuccessPlanRepository(db))

    async def create_plan(self, req: SuccessPlanCreate, tenant_id: str) -> CustomerSuccessPlan:
        data = req.model_dump(exclude_unset=True)
        if "goals" not in data or data["goals"] is None:
            data["goals"] = ["Complete onboarding setup", "Configure team access", "Import existing CRM records"]
            
        data["health_score"] = 85
        data["health_grade"] = "good"
        plan = await self.repository.create(data, tenant_id=tenant_id)

        # Standard onboarding milestones
        milestones = [
            "Technical Kickoff & Architecture Review",
            "Data Migration (Contacts & Companies)",
            "Sales Pipeline Configuration",
            "Team Training & User Onboarding"
        ]
        for m in milestones:
            self.repository.db.add(OnboardingMilestone(
                plan_id=plan.id,
                title=m,
                is_completed=False
            ))
        await self.repository.db.flush()

        return await self.repository.get_with_milestones(plan.id, tenant_id)

    async def recalculate_health_score(self, plan_id: str, tenant_id: str) -> CustomerSuccessPlan:
        plan = await self.repository.get_with_milestones(plan_id, tenant_id)
        if not plan:
            return None

        # 1. Milestone progress
        completed_m = len([m for m in plan.milestones if m.is_completed])
        total_m = len(plan.milestones) or 1
        milestone_ratio = completed_m / total_m

        # 2. Open urgent/high support tickets count
        query = select(func.count(Ticket.id)).where(
            Ticket.company_id == plan.company_id,
            Ticket.status.in_(["open", "pending", "in_progress"]),
            Ticket.priority.in_(["urgent", "high"]),
            Ticket.tenant_id == tenant_id,
            Ticket.is_deleted == False
        )
        res = await self.repository.db.execute(query)
        urgent_tickets = res.scalar() or 0

        # Health score formula
        base_score = 70 + int(milestone_ratio * 30) - (urgent_tickets * 15)
        score = max(0, min(100, base_score))

        if score >= 75:
            grade = "good"
            status = "active"
            churn_reason = None
        elif score >= 50:
            grade = "warning"
            status = "active"
            churn_reason = "Elevated support tickets or incomplete onboarding milestones"
        else:
            grade = "critical"
            status = "at_risk"
            churn_reason = "High volume of critical support issues"

        return await self.repository.update(plan, {
            "health_score": score,
            "health_grade": grade,
            "status": status,
            "churn_risk_reason": churn_reason
        })
