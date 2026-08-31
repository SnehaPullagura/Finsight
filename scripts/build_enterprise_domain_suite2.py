import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/domain_services/contract_generator.py
    write_file("backend/app/domain_services/contract_generator.py", """from datetime import date, timedelta
from typing import Any, Dict, List, Optional

class ContractClauseBuilder:
    STANDARD_CLAUSES = {
        "confidentiality": "Each party agrees to hold the other party's Confidential Information in strict confidence and not to disclose such Confidential Information to any third party.",
        "intellectual_property": "ClientFlow CRM retains all right, title, and interest in and to the platform, including all modifications, enhancements, and intellectual property rights.",
        "service_level_agreement": "Provider warrants that the Production Cloud Service shall maintain an uptime SLA of 99.9% in each calendar month.",
        "data_protection_gdpr": "Both parties shall comply with all applicable requirements of the General Data Protection Regulation (EU) 2016/679 (GDPR).",
        "governing_law": "This Agreement shall be governed by and construed in accordance with the laws of the State of Delaware, without giving effect to any choice of law rules."
    }

    @staticmethod
    def generate_contract_document(
        customer_name: str,
        total_contract_value: float,
        term_months: int,
        currency: str = "USD",
        custom_clauses: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        start_date = date.today()
        end_date = start_date + timedelta(days=term_months * 30)

        clauses = dict(ContractClauseBuilder.STANDARD_CLAUSES)
        if custom_clauses:
            for i, c in enumerate(custom_clauses, 1):
                clauses[f"special_condition_{i}"] = c

        contract_payload = {
            "title": f"Enterprise Cloud Platform Master Services Agreement — {customer_name}",
            "customer_legal_name": customer_name,
            "effective_date": start_date.isoformat(),
            "termination_date": end_date.isoformat(),
            "contract_value": {
                "total_amount": total_contract_value,
                "currency": currency,
                "billing_schedule": "Annual Upfront" if term_months >= 12 else "Monthly Recurring"
            },
            "terms_and_conditions": clauses,
            "signature_required": True,
            "status": "ready_for_signature"
        }
        return contract_payload
""")

    # 2. backend/app/domain_services/sla_monitoring_engine.py
    write_file("backend/app/domain_services/sla_monitoring_engine.py", """from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional

class SLAMonitoringEngine:
    PRIORITY_TARGETS_HOURS = {
        "critical": {"first_response_hours": 1, "resolution_hours": 4},
        "high": {"first_response_hours": 2, "resolution_hours": 8},
        "medium": {"first_response_hours": 8, "resolution_hours": 24},
        "low": {"first_response_hours": 24, "resolution_hours": 72}
    }

    @staticmethod
    def evaluate_ticket_sla(
        created_at: datetime,
        priority: str,
        first_response_at: Optional[datetime] = None,
        resolved_at: Optional[datetime] = None,
        current_time: Optional[datetime] = None
    ) -> Dict[str, Any]:
        now = current_time or datetime.now(timezone.utc)
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)
        if first_response_at and first_response_at.tzinfo is None:
            first_response_at = first_response_at.replace(tzinfo=timezone.utc)
        if resolved_at and resolved_at.tzinfo is None:
            resolved_at = resolved_at.replace(tzinfo=timezone.utc)

        target = SLAMonitoringEngine.PRIORITY_TARGETS_HOURS.get(priority.lower(), SLAMonitoringEngine.PRIORITY_TARGETS_HOURS["medium"])
        resp_deadline = created_at + timedelta(hours=target["first_response_hours"])
        res_deadline = created_at + timedelta(hours=target["resolution_hours"])

        # Check response SLA
        if first_response_at:
            resp_breached = first_response_at > resp_deadline
            resp_status = "breached" if resp_breached else "met"
        else:
            resp_breached = now > resp_deadline
            resp_status = "breached" if resp_breached else "pending"

        # Check resolution SLA
        if resolved_at:
            res_breached = resolved_at > res_deadline
            res_status = "breached" if res_breached else "met"
        else:
            res_breached = now > res_deadline
            res_status = "breached" if res_breached else "in_progress"

        return {
            "priority": priority,
            "response_sla": {
                "target_hours": target["first_response_hours"],
                "deadline": resp_deadline.isoformat(),
                "status": resp_status,
                "is_breached": resp_breached
            },
            "resolution_sla": {
                "target_hours": target["resolution_hours"],
                "deadline": res_deadline.isoformat(),
                "status": res_status,
                "is_breached": res_breached
            },
            "overall_breached": resp_breached or res_breached
        }
""")

    # 3. backend/app/domain_services/customer_health_scorer.py
    write_file("backend/app/domain_services/customer_health_scorer.py", """from typing import Dict, List, Optional

class CustomerHealthScorer:
    @staticmethod
    def calculate_health_score(
        login_frequency_weekly: int,
        active_user_ratio: float, # 0.0 - 1.0
        open_critical_tickets: int,
        feature_adoption_count: int,
        nps_score: Optional[int] = None
    ) -> Dict[str, Any]:
        score = 50 # Baseline midpoint

        # 1. Login Frequency (+/- 15 pts)
        if login_frequency_weekly >= 5:
            score += 15
        elif login_frequency_weekly >= 2:
            score += 5
        else:
            score -= 15

        # 2. Active User Ratio (+/- 20 pts)
        if active_user_ratio >= 0.80:
            score += 20
        elif active_user_ratio >= 0.50:
            score += 10
        elif active_user_ratio < 0.25:
            score -= 20

        # 3. Support Tickets (-10 per critical)
        score -= min(30, open_critical_tickets * 15)

        # 4. Feature Adoption (+/- 15 pts)
        score += min(15, feature_adoption_count * 3)

        # 5. NPS Score (+/- 10 pts)
        if nps_score is not None:
            if nps_score >= 9:
                score += 10
            elif nps_score <= 6:
                score -= 10

        final_score = max(0, min(100, score))

        if final_score >= 80:
            grade = "good"
            risk_level = "low"
        elif final_score >= 50:
            grade = "average"
            risk_level = "medium"
        else:
            grade = "poor"
            risk_level = "high"

        return {
            "health_score": final_score,
            "health_grade": grade,
            "churn_risk": risk_level,
            "metrics_breakdown": {
                "login_frequency": login_frequency_weekly,
                "active_user_ratio": active_user_ratio,
                "open_critical_tickets": open_critical_tickets,
                "feature_adoption": feature_adoption_count,
                "nps": nps_score
            }
        }
""")

    print("Contract, SLA, and Health domain services created.")

if __name__ == '__main__':
    run()
