import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/enterprise_reporting_engine.py
    write_file("backend/app/enterprise/enterprise_reporting_engine.py", """from datetime import date, timedelta
from typing import Any, Dict, List, Optional
from collections import defaultdict

class EnterpriseReportingEngine:
    @staticmethod
    def generate_sales_rep_leaderboard(deals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        rep_stats = defaultdict(lambda: {"rep_name": "", "deals_won": 0, "revenue_won": 0.0, "open_deals": 0, "open_pipeline": 0.0})

        for d in deals:
            rep_id = d.get("owner_id") or "unassigned"
            name = d.get("owner_name") or f"Rep {rep_id[:8]}"
            status = (d.get("status") or "open").lower()
            val = float(d.get("value", 0.0))

            rep_stats[rep_id]["rep_name"] = name
            if status == "won":
                rep_stats[rep_id]["deals_won"] += 1
                rep_stats[rep_id]["revenue_won"] += val
            elif status == "open":
                rep_stats[rep_id]["open_deals"] += 1
                rep_stats[rep_id]["open_pipeline"] += val

        leaderboard = []
        for rep_id, s in rep_stats.items():
            win_rate = (s["deals_won"] / max(1, s["deals_won"] + s["open_deals"])) * 100.0
            leaderboard.append({
                "rep_id": rep_id,
                "rep_name": s["rep_name"],
                "deals_won_count": s["deals_won"],
                "total_revenue_won": round(s["revenue_won"], 2),
                "open_pipeline_value": round(s["open_pipeline"], 2),
                "win_rate_percentage": round(win_rate, 1)
            })

        return sorted(leaderboard, key=lambda x: x["total_revenue_won"], reverse=True)
""")

    # 2. backend/app/enterprise/enterprise_security_firewall.py
    write_file("backend/app/enterprise/enterprise_security_firewall.py", """from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional
from collections import defaultdict

class EnterpriseSecurityFirewall:
    def __init__(self, max_attempts: int = 5, lockout_minutes: int = 15):
        self.max_attempts = max_attempts
        self.lockout_minutes = lockout_minutes
        self._login_attempts = defaultdict(list)
        self._locked_ips = {}

    def record_attempt(self, ip_address: str, success: bool) -> bool:
        now = datetime.now(timezone.utc)
        
        # Clean up expired lockouts
        if ip_address in self._locked_ips and now > self._locked_ips[ip_address]:
            del self._locked_ips[ip_address]

        if ip_address in self._locked_ips:
            return False # Blocked

        if success:
            self._login_attempts[ip_address] = []
            return True

        # Failed attempt
        self._login_attempts[ip_address].append(now)
        recent_failures = [t for t in self._login_attempts[ip_address] if now - t < timedelta(minutes=self.lockout_minutes)]
        self._login_attempts[ip_address] = recent_failures

        if len(recent_failures) >= self.max_attempts:
            self._locked_ips[ip_address] = now + timedelta(minutes=self.lockout_minutes)
            return False

        return True
""")

    # 3. backend/app/enterprise/enterprise_customer_success_playbooks.py
    write_file("backend/app/enterprise/enterprise_customer_success_playbooks.py", """from typing import Any, Dict, List

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
""")

    print("Created reporting engine, security firewall, and success playbooks.")

if __name__ == '__main__':
    run()
