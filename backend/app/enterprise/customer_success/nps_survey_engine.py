from typing import Any, Dict, List, Optional

class NetPromoterScoreEngine:
    @staticmethod
    def calculate_nps(responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not responses:
            return {"nps_score": 0, "promoters_pct": 0.0, "passives_pct": 0.0, "detractors_pct": 0.0, "total_responses": 0}

        promoters = [r for r in responses if int(r.get("score", 0)) >= 9]
        passives = [r for r in responses if 7 <= int(r.get("score", 0)) <= 8]
        detractors = [r for r in responses if int(r.get("score", 0)) <= 6]

        total = len(responses)
        promoters_pct = round((len(promoters) / float(total)) * 100.0, 1)
        passives_pct = round((len(passives) / float(total)) * 100.0, 1)
        detractors_pct = round((len(detractors) / float(total)) * 100.0, 1)

        nps = int(round(promoters_pct - detractors_pct))

        return {
            "nps_score": nps,
            "promoters_count": len(promoters),
            "promoters_percentage": promoters_pct,
            "passives_count": len(passives),
            "passives_percentage": passives_pct,
            "detractors_count": len(detractors),
            "detractors_percentage": detractors_pct,
            "total_responses": total,
            "benchmark_rating": "Excellent" if nps >= 50 else "Good" if nps >= 30 else "Needs Improvement" if nps >= 0 else "Critical"
        }
