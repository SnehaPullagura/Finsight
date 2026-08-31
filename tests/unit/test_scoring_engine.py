import pytest
from backend.app.models.lead import Lead, LeadScoringRule
from backend.app.services.lead import LeadQualificationEngine
from backend.app.models.automation import WorkflowCondition
from backend.app.services.automation import AutomationEngine

def test_lead_qualification_budget_scoring():
    lead = Lead(
        id="lead-1",
        tenant_id="t1",
        first_name="Jane",
        last_name="Doe",
        email="jane@example.com",
        estimated_budget=75000.0,
        employee_count=150,
        industry="Technology",
        intent_score=80,
        engagement_count=5
    )

    rule1 = LeadScoringRule(
        name="High Budget",
        criteria_type="budget",
        operator="gt",
        target_value="50000",
        score_weight=30,
        is_active=True
    )

    rule2 = LeadScoringRule(
        name="Enterprise Size",
        criteria_type="company_size",
        operator="gte",
        target_value="100",
        score_weight=25,
        is_active=True
    )

    score, grade, breakdown = LeadQualificationEngine.calculate_score(lead, [rule1, rule2])
    # Base 20 + 30 + 25 = 75
    assert score == 75
    assert grade == "B"
    assert "High Budget" in breakdown
    assert "Enterprise Size" in breakdown

def test_automation_condition_evaluation():
    cond = WorkflowCondition(
        field_path="value",
        operator="gt",
        target_value="100000"
    )
    assert AutomationEngine.evaluate_condition({"value": 150000}, cond) is True
    assert AutomationEngine.evaluate_condition({"value": 50000}, cond) is False
