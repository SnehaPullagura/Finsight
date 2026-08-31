from typing import Any, Dict, List

class EnterpriseCustomerSuccessPlaybooks:
    @staticmethod
    def get_playbooks() -> List[Dict[str, Any]]:
        return [
            {
                "id": "pb-onboarding-30-day",
                "name": "30-Day White-Glove Enterprise Onboarding Playbook",
                "milestones": [
                    {"day": 1, "task": "Welcome Kickoff Call & Executive Introductions"},
                    {"day": 7, "task": "Identity Provider (Okta/Azure AD) SSO Verification"},
                    {"day": 14, "task": "Legacy Data Migration & Custom Field Mapping"},
                    {"day": 21, "task": "Sales Team Training & Workflow Certification"},
                    {"day": 30, "task": "Executive Go-Live Sign-Off & CSAT Survey"}
                ]
            },
            {
                "id": "pb-churn-recovery-fast",
                "name": "High-Priority Account Churn Recovery Playbook",
                "milestones": [
                    {"day": 1, "task": "Immediate Executive Outreach by VP of Customer Success"},
                    {"day": 3, "task": "Root Cause Technical & Adoption Review"},
                    {"day": 7, "task": "Remediation Action Plan Deployment & Health Monitoring"},
                    {"day": 14, "task": "Follow-Up Review & Health Score Re-evaluation"}
                ]
            }
        ]
