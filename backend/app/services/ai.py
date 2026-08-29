from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.exceptions import EntityNotFoundException, ValidationException
from backend.app.repositories.lead import LeadRepository
from backend.app.repositories.deal import DealRepository
from backend.app.schemas.ai import (
    AILeadSummaryResponse,
    AIDealRiskAnalysisResponse,
    AIEmailDraftRequest,
    AIEmailDraftResponse,
    AINLQueryRequest,
    AINLQueryResponse
)

class AIAssistantService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.lead_repo = LeadRepository(session)
        self.deal_repo = DealRepository(session)

    async def summarize_lead(self, lead_id: str, tenant_id: str) -> AILeadSummaryResponse:
        lead = await self.lead_repo.get_by_id(lead_id, tenant_id=tenant_id)
        if not lead:
            raise EntityNotFoundException("Lead", lead_id)

        # Heuristic predictive synthesis
        fit_score = 60
        strengths = []
        risks = []
        next_steps = []

        if lead.estimated_budget and lead.estimated_budget > 10000:
            fit_score += 20
            strengths.append(f"Strong budget indication: ${lead.estimated_budget:,.2f}")
        else:
            risks.append("Unconfirmed or low estimated budget")

        if lead.email and "@" in lead.email and not lead.email.endswith(("gmail.com", "yahoo.com", "hotmail.com")):
            fit_score += 15
            strengths.append("Verified corporate business domain")
        else:
            risks.append("Personal or unverified email domain")

        if lead.status in ["qualified", "contacted"]:
            fit_score += 10
            next_steps.append("Schedule product demonstration call")
        else:
            next_steps.append("Initiate introductory discovery outreach")

        fit_score = min(max(fit_score, 10), 98)

        summary = f"Lead {lead.first_name} {lead.last_name} from {lead.company_name or 'Independent'} scored at {fit_score}/100 fit rating."

        return AILeadSummaryResponse(
            lead_id=lead.id,
            summary=summary,
            key_strengths=strengths or ["Active interest registered"],
            risk_factors=risks or ["No high risk factors identified"],
            suggested_next_steps=next_steps,
            estimated_fit_score=fit_score
        )

    async def analyze_deal_risk(self, deal_id: str, tenant_id: str) -> AIDealRiskAnalysisResponse:
        deal = await self.deal_repo.get_by_id(deal_id, tenant_id=tenant_id)
        if not deal:
            raise EntityNotFoundException("Deal", deal_id)

        win_prob = deal.probability if deal.probability is not None else 50
        risks = []
        recs = []

        if win_prob < 40:
            risk_level = "high"
            risks.append("Low win probability estimate based on stage progress")
            recs.append("Conduct executive sponsor alignment review")
        elif win_prob < 70:
            risk_level = "medium"
            risks.append("Pending decision-maker consensus")
            recs.append("Share customer case studies and ROI calculation sheet")
        else:
            risk_level = "low"
            recs.append("Prepare final MSA and security compliance documentation")

        momentum = max(20, min(100, int(win_prob * 1.1)))

        return AIDealRiskAnalysisResponse(
            deal_id=deal.id,
            deal_name=deal.name,
            win_probability_pct=win_prob,
            risk_level=risk_level,
            identified_risks=risks or ["Stage progression normal"],
            deal_momentum_score=momentum,
            actionable_recommendations=recs
        )

    async def draft_email(self, req: AIEmailDraftRequest) -> AIEmailDraftResponse:
        objective = req.objective.lower()
        name = req.recipient_name
        topic = req.context_topic

        if objective == "schedule_meeting":
            subject = f"Connecting regarding {topic} - Brief intro?"
            body = f"Hi {name},\n\nI hope you are having a productive week. Following up on {topic}, I would love to find 15 minutes to share how we can support your initiatives.\n\nDo you have some time this Thursday or Friday?"
            cta = "Book a 15-minute sync on our calendar"
        elif objective == "proposal_review":
            subject = f"Reviewing proposal details for {topic}"
            body = f"Hi {name},\n\nWe have prepared the tailored proposal covering {topic}. I have outlined the scope, milestones, and commercial terms for your team.\n\nPlease let me know if you would like any adjustments."
            cta = "Review proposal and confirm next steps"
        elif objective == "renewal_checkin":
            subject = f"Checking in on your {topic} experience & upcoming renewal"
            body = f"Hi {name},\n\nThank you for being a valued partner. As your subscription milestone approaches for {topic}, I wanted to ensure you are maximizing value and discuss our updated feature roadmap."
            cta = "Schedule renewal review session"
        else:
            subject = f"Following up on {topic}"
            body = f"Hi {name},\n\nI wanted to quickly follow up regarding {topic}. Please let me know if you have any questions or if we can assist further."
            cta = "Reply to schedule next steps"

        return AIEmailDraftResponse(
            subject=subject,
            body_text=body,
            call_to_action=cta
        )

    async def process_nl_query(self, req: AINLQueryRequest) -> AINLQueryResponse:
        query = req.query_text.lower()
        if "deal" in query or "pipeline" in query or "revenue" in query:
            entity = "deal"
            intent = "filter_deals_by_criteria"
            filters = {"status": "open", "order_by": "value_desc"}
            sql = "SELECT * FROM deals WHERE status = 'open' ORDER BY value DESC LIMIT 20;"
            insights = "Extracted open deals prioritized by deal monetary value."
        elif "lead" in query or "prospect" in query:
            entity = "lead"
            intent = "filter_leads_by_status"
            filters = {"status": "qualified"}
            sql = "SELECT * FROM leads WHERE status = 'qualified' ORDER BY created_at DESC LIMIT 20;"
            insights = "Identified qualified leads awaiting sales engagement."
        else:
            entity = "contact"
            intent = "search_contacts"
            filters = {"query": req.query_text}
            sql = f"SELECT * FROM contacts WHERE name ILIKE '%{req.query_text}%' LIMIT 20;"
            insights = "Generic CRM entity query parsed."

        return AINLQueryResponse(
            interpreted_intent=intent,
            target_entity=entity,
            applied_filters=filters,
            sql_or_search_expression=sql,
            insights_summary=insights
        )
