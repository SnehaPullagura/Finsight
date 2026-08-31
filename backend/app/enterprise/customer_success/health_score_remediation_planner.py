from typing import Any, Dict, List, Optional

class HealthScoreRemediationPlanner:
    @staticmethod
    def generate_intervention_play(company: Dict[str, Any], health_score: int, primary_failing_metric: str) -> Dict[str, Any]:
        cid = company.get("id")
        cname = company.get("name")

        playbooks = {
            "low_product_usage": {
                "action_title": "Product Re-Engagement & Feature Certification",
                "recommended_steps": [
                    "Audit unused license seats across customer teams",
                    "Conduct dedicated admin onboarding refresher workshop",
                    "Share personalized ROI workflow automation dashboard"
                ]
            },
            "support_ticket_backlog": {
                "action_title": "Technical Escalation & Bug Remediation Sprint",
                "recommended_steps": [
                    "Assign dedicated Tier 3 Support Engineer",
                    "Conduct daily standup on open blockers",
                    "Provide weekly executive status updates"
                ]
            },
            "detractor_nps": {
                "action_title": "Executive Alignment & Relationship Recovery",
                "recommended_steps": [
                    "Schedule VP-level listening session within 48 hours",
                    "Document mutual success plan with clear deliverable milestones",
                    "Offer roadmap influence on key requested enterprise features"
                ]
            }
        }

        play = playbooks.get(primary_failing_metric, playbooks["low_product_usage"])

        return {
            "company_id": cid,
            "company_name": cname,
            "current_health_score": health_score,
            "failing_metric": primary_failing_metric,
            "intervention_plan": play,
            "target_recovery_health_score": 85
        }
