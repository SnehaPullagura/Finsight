from datetime import date
from typing import Any, Dict, List, Optional

class MarketingCohortBuilder:
    @staticmethod
    def segment_audience(contacts: List[Dict[str, Any]], criteria: Dict[str, Any]) -> Dict[str, Any]:
        matched_contacts = []
        excluded_contacts = []

        target_industry = criteria.get("industry")
        min_revenue = float(criteria.get("min_annual_revenue", 0.0))
        target_lifecycle = criteria.get("lifecycle_stage")

        for c in contacts:
            ind = c.get("industry")
            rev = float(c.get("annual_revenue", 0.0))
            stage = c.get("lifecycle_stage")

            match = True
            if target_industry and ind != target_industry:
                match = False
            if rev < min_revenue:
                match = False
            if target_lifecycle and stage != target_lifecycle:
                match = False

            if match:
                matched_contacts.append(c)
            else:
                excluded_contacts.append(c)

        return {
            "segment_name": criteria.get("name", "Custom Segment"),
            "matched_count": len(matched_contacts),
            "excluded_count": len(excluded_contacts),
            "matched_audience": matched_contacts[:50]
        }
