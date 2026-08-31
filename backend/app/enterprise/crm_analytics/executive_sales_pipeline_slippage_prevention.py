from typing import Any, Dict, List, Optional

class SlippagePreventionPlaybookEngine:
    @staticmethod
    def prescribe_prevention_play(deal: Dict[str, Any], slippage_risk_score: int) -> Dict[str, Any]:
        dname = deal.get("name")
        val = float(deal.get("value", 0.0))

        if slippage_risk_score >= 70:
            actions = [
                "Schedule immediate CRO-to-CEO peer negotiation sync",
                "Offer customized payment schedule ramp",
                "Dispatch technical solutions engineer for immediate security review sign-off"
            ]
        elif slippage_risk_score >= 40:
            actions = [
                "Conduct champion check-in call within 24 hours",
                "Send executive summary briefing deck to economic buyer"
            ]
        else:
            actions = ["Maintain standard sales cadence"]

        return {
            "deal_name": dname,
            "deal_value": val,
            "risk_score": slippage_risk_score,
            "prescribed_intervention_actions": actions,
            "is_executive_escalation_triggered": slippage_risk_score >= 70
        }
