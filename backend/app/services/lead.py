from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.exceptions import ConflictException, EntityNotFoundException, ValidationException
from backend.app.models.lead import Lead, LeadScoringRule
from backend.app.repositories.lead import LeadRepository, LeadScoringRuleRepository
from backend.app.repositories.contact import ContactRepository
from backend.app.repositories.company import CompanyRepository
from backend.app.services.base import BaseService
from backend.app.schemas.lead import (
    LeadCreate,
    LeadUpdate,
    LeadConvertRequest,
    LeadConvertResponse,
    LeadScoringRuleCreate
)

class LeadQualificationEngine:
    @staticmethod
    def evaluate_rule(lead: Lead, rule: LeadScoringRule) -> int:
        field_val = None
        if rule.criteria_type == "budget":
            field_val = float(lead.estimated_budget or 0)
        elif rule.criteria_type == "company_size":
            field_val = int(lead.employee_count or 0)
        elif rule.criteria_type == "intent":
            field_val = int(lead.intent_score or 0)
        elif rule.criteria_type == "engagement":
            field_val = int(lead.engagement_count or 0)
        elif rule.criteria_type == "industry":
            field_val = (lead.industry or "").lower()

        if field_val is None:
            return 0

        target = rule.target_value
        op = rule.operator.lower()

        try:
            if op in ["gt", "gte", "lt", "lte", "eq"] and isinstance(field_val, (int, float)):
                target_num = float(target)
                if op == "gt" and field_val > target_num:
                    return rule.score_weight
                elif op == "gte" and field_val >= target_num:
                    return rule.score_weight
                elif op == "lt" and field_val < target_num:
                    return rule.score_weight
                elif op == "lte" and field_val <= target_num:
                    return rule.score_weight
                elif op == "eq" and field_val == target_num:
                    return rule.score_weight
            elif op == "contains" and isinstance(field_val, str):
                if target.lower() in field_val:
                    return rule.score_weight
            elif op == "eq" and isinstance(field_val, str):
                if target.lower() == field_val:
                    return rule.score_weight
        except Exception:
            return 0
        return 0

    @classmethod
    def calculate_score(cls, lead: Lead, rules: List[LeadScoringRule]) -> Tuple[int, str, Dict[str, Any]]:
        total_score = 20 # Base score
        breakdown = {}

        if rules:
            for rule in rules:
                points = cls.evaluate_rule(lead, rule)
                if points > 0:
                    total_score += points
                    breakdown[rule.name] = points
        else:
            # Built-in heuristic when no custom tenant rules configured
            if (lead.estimated_budget or 0) >= 50000:
                total_score += 30
                breakdown["Enterprise Budget"] = 30
            if (lead.intent_score or 0) >= 50:
                total_score += 25
                breakdown["High Intent"] = 25
            if (lead.employee_count or 0) >= 50:
                total_score += 15
                breakdown["Target Scale"] = 15

        total_score = max(0, min(100, total_score))
        
        if total_score >= 80:
            grade = "A"
        elif total_score >= 65:
            grade = "B"
        elif total_score >= 50:
            grade = "C"
        elif total_score >= 35:
            grade = "D"
        else:
            grade = "F"

        return total_score, grade, breakdown

class LeadService(BaseService[Lead, LeadRepository]):
    def __init__(self, db: AsyncSession):
        super().__init__(LeadRepository(db))
        self.db = db
        self.rule_repo = LeadScoringRuleRepository(db)
        self.contact_repo = ContactRepository(db)
        self.company_repo = CompanyRepository(db)

    async def create_lead(self, schema_in: LeadCreate, tenant_id: str, actor_id: Optional[str] = None) -> Lead:
        existing = await self.repository.get_by_email(schema_in.email, tenant_id=tenant_id)
        if existing:
            raise ConflictException(f"Lead with email '{schema_in.email}' already exists.")

        data = schema_in.model_dump(exclude_unset=True)
        if "custom_fields" not in data or data["custom_fields"] is None:
            data["custom_fields"] = {}
            
        lead = await self.repository.create(data, tenant_id=tenant_id)
        
        # Calculate initial score
        rules = await self.rule_repo.list_active_rules(tenant_id)
        score, grade, details = LeadQualificationEngine.calculate_score(lead, rules)
        lead = await self.repository.update(lead, {
            "score": score,
            "qualification_grade": grade,
            "qualification_details": details
        })
        return lead

    async def qualify_lead(self, lead_id: str, tenant_id: str) -> Lead:
        lead = await self.get(lead_id, tenant_id=tenant_id)
        rules = await self.rule_repo.list_active_rules(tenant_id)
        score, grade, details = LeadQualificationEngine.calculate_score(lead, rules)
        
        new_status = "qualified" if score >= 50 else "unqualified"
        return await self.repository.update(lead, {
            "score": score,
            "qualification_grade": grade,
            "qualification_details": details,
            "status": new_status
        })

    async def convert_lead(self, lead_id: str, req: LeadConvertRequest, tenant_id: str, actor_id: Optional[str] = None) -> LeadConvertResponse:
        lead = await self.get(lead_id, tenant_id=tenant_id)
        if lead.status == "converted":
            raise ConflictException("Lead has already been converted.")

        company_id = None
        if lead.company_name:
            company = await self.company_repo.create({
                "name": lead.company_name,
                "industry": lead.industry,
                "employee_count": lead.employee_count,
                "annual_revenue": lead.estimated_budget,
                "owner_id": lead.owner_id
            }, tenant_id=tenant_id)
            company_id = company.id

        contact = await self.contact_repo.create({
            "first_name": lead.first_name,
            "last_name": lead.last_name,
            "email": lead.email,
            "phone": lead.phone,
            "title": lead.title,
            "company_id": company_id,
            "owner_id": lead.owner_id,
            "lifecycle_stage": "opportunity" if req.create_deal else "lead",
            "lead_source": lead.source
        }, tenant_id=tenant_id)

        deal_id = None
        if req.create_deal:
            from backend.app.models.deal import Deal
            deal_name = req.deal_name or f"Deal with {lead.company_name or lead.first_name + ' ' + lead.last_name}"
            deal_val = req.deal_value if req.deal_value is not None else (lead.estimated_budget or 10000.0)
            
            # Simple direct insertion for deal
            deal = Deal(
                tenant_id=tenant_id,
                name=deal_name,
                company_id=company_id,
                contact_id=contact.id,
                owner_id=lead.owner_id,
                value=deal_val,
                probability=40,
                stage_id=req.stage_id or "default_stage",
                pipeline_id=req.pipeline_id or "default_pipeline"
            )
            self.db.add(deal)
            await self.db.flush()
            await self.db.refresh(deal)
            deal_id = deal.id

        # Update lead
        await self.repository.update(lead, {
            "status": "converted",
            "converted_at": datetime.utcnow(),
            "converted_contact_id": contact.id,
            "converted_company_id": company_id,
            "converted_deal_id": deal_id
        })

        return LeadConvertResponse(
            lead_id=lead.id,
            contact_id=contact.id,
            company_id=company_id,
            deal_id=deal_id,
            message="Lead successfully converted."
        )
