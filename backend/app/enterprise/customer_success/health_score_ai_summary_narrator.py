from typing import Any, Dict, Optional

class HealthScoreNarrativeGenerator:
    @staticmethod
    def generate_executive_account_narrative(account: Dict[str, Any]) -> Dict[str, Any]:
        cname = account.get("name")
        health = int(account.get("health_score", 50))
        nps = int(account.get("nps", 8))
        arr = account.get("current_arr", "$100,000")

        if health >= 85:
            summary = f"{cname} is an elite champion account ({health}/100) with strong NPS ({nps}/10) and expanding ARR ({arr}). Ideal candidate for case study and advisory board."
        elif health >= 65:
            summary = f"{cname} is in stable health ({health}/100). Recommend scheduling standard quarterly business review to maintain momentum."
        else:
            summary = f"{cname} is currently at elevated risk ({health}/100). Executive outreach and dedicated technical triage recommended immediately."

        return {
            "account_name": cname,
            "health_score": health,
            "executive_summary_narrative": summary,
            "urgency": "High" if health < 65 else "Low"
        }
