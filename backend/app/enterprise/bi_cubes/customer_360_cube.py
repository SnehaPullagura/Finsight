from datetime import date, datetime
from typing import Any, Dict, List, Optional
from collections import defaultdict

class Customer360Cube:
    @staticmethod
    def aggregate_customer_profile(
        company: Dict[str, Any],
        contacts: List[Dict[str, Any]],
        deals: List[Dict[str, Any]],
        contracts: List[Dict[str, Any]],
        tickets: List[Dict[str, Any]],
        activities: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        cid = company.get("id")
        
        # Financial rollups
        won_deals = [d for d in deals if d.get("status") == "won"]
        total_lifetime_revenue = sum(float(d.get("value", 0.0)) for d in won_deals)
        open_pipeline_value = sum(float(d.get("value", 0.0)) for d in deals if d.get("status") == "open")
        
        active_contracts = [c for c in contracts if c.get("status") == "active"]
        annual_recurring_revenue = sum(float(c.get("contract_value", {}).get("total_amount", 0.0)) for c in active_contracts)

        # Support & Satisfaction rollups
        open_tickets = [t for t in tickets if t.get("status") in ["open", "in_progress", "pending"]]
        critical_tickets = [t for t in open_tickets if (t.get("priority") or "").lower() == "critical"]
        sla_breached_count = sum(1 for t in tickets if t.get("is_sla_breached"))

        # Activity Recency
        last_contact_date = max([a.get("created_at", "") for a in activities] or ["N/A"])

        # Health Scoring (0-100)
        health_score = 100
        if critical_tickets:
            health_score -= 30
        if sla_breached_count > 0:
            health_score -= 20
        if not activities:
            health_score -= 25
        health_score = max(0, min(100, health_score))

        return {
            "company_id": cid,
            "company_name": company.get("name"),
            "industry": company.get("industry"),
            "tier": company.get("tier", "growth"),
            "key_metrics": {
                "total_contacts_count": len(contacts),
                "total_lifetime_revenue": round(total_lifetime_revenue, 2),
                "current_arr": round(annual_recurring_revenue, 2),
                "open_pipeline_value": round(open_pipeline_value, 2),
                "open_tickets_count": len(open_tickets),
                "critical_tickets_count": len(critical_tickets),
                "sla_breach_count": sla_breached_count,
                "health_score": health_score,
                "health_grade": "A" if health_score >= 80 else "B" if health_score >= 60 else "C" if health_score >= 40 else "F",
                "last_activity_timestamp": last_contact_date
            },
            "summary_status": "healthy" if health_score >= 70 else "at_risk" if health_score >= 45 else "critical"
        }
