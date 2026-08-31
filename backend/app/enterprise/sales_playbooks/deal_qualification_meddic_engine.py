from typing import Any, Dict, List, Optional

class MEDDPICCEngine:
    CRITERIA_WEIGHTS = {
        "metrics": 15,          # Quantified economic impact ($ ROI)
        "economic_buyer": 20,   # Access to budget signoff authority
        "decision_criteria": 10,# Defined technical & business requirements
        "decision_process": 10, # Clear timeline & approval steps
        "paper_process": 15,    # Legal, procurement, & security review steps
        "identify_pain": 10,    # Compelling pain & cost of inaction
        "champion": 15,         # Internal advocate with influence
        "competition": 5        # Identified competitors & differentiation
    }

    @staticmethod
    def evaluate_deal_meddic_health(evaluations: Dict[str, bool]) -> Dict[str, Any]:
        total_score = 0
        passed_criteria = []
        missing_criteria = []

        for criterion, weight in MEDDPICCEngine.CRITERIA_WEIGHTS.items():
            if evaluations.get(criterion, False):
                total_score += weight
                passed_criteria.append(criterion)
            else:
                missing_criteria.append(criterion)

        qualification_level = "Fully Qualified" if total_score >= 85 else "Partially Qualified" if total_score >= 60 else "Unqualified / High Risk"
        is_commit_ready = total_score >= 80 and evaluations.get("economic_buyer") and evaluations.get("champion")

        return {
            "total_meddic_score": total_score,
            "qualification_level": qualification_level,
            "is_commit_ready": bool(is_commit_ready),
            "passed_criteria": passed_criteria,
            "missing_criteria": missing_criteria
        }
