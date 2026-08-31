import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/analytics/data_warehouse_schemas.py
    write_file("backend/app/analytics/data_warehouse_schemas.py", """from datetime import date, datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class DimTime(BaseModel):
    date_key: int # YYYYMMDD
    full_date: date
    day_of_week: int
    day_name: str
    month: int
    month_name: str
    quarter: int
    year: int
    is_weekend: bool
    is_holiday: bool = False

class DimCompany(BaseModel):
    company_key: str
    name: str
    industry: str
    tier: str
    country: str
    city: str
    employee_range: str
    annual_revenue_band: str

class DimContact(BaseModel):
    contact_key: str
    company_key: str
    first_name: str
    last_name: str
    email: str
    title: str
    lifecycle_stage: str
    lead_source: str

class DimSalesRep(BaseModel):
    rep_key: str
    first_name: str
    last_name: str
    email: str
    team_name: str
    region: str
    quota_tier: str

class FactDealSnapshot(BaseModel):
    deal_key: str
    date_key: int
    company_key: str
    contact_key: str
    rep_key: str
    pipeline_key: str
    stage_key: str
    deal_amount: float
    probability_percentage: float
    weighted_amount: float
    is_won: bool = False
    is_lost: bool = False
    days_in_current_stage: int = 0
    total_sales_cycle_days: int = 0

class FactSubscriptionMRR(BaseModel):
    subscription_key: str
    date_key: int
    company_key: str
    plan_key: str
    mrr_amount: float
    arr_amount: float
    expansion_mrr: float = 0.0
    contraction_mrr: float = 0.0
    churn_mrr: float = 0.0
    net_new_mrr: float = 0.0

class FactSupportTicket(BaseModel):
    ticket_key: str
    date_key: int
    company_key: str
    contact_key: str
    assigned_rep_key: str
    priority: str
    category: str
    resolution_time_hours: float
    first_response_time_hours: float
    sla_response_breached: bool = False
    sla_resolution_breached: bool = False
    csat_score: Optional[int] = None
""")

    # 2. backend/app/analytics/olap_cubes.py
    write_file("backend/app/analytics/olap_cubes.py", """from typing import Any, Dict, List, Optional, Tuple
from collections import defaultdict

class InMemOLAPCube:
    def __init__(self, fact_records: List[Dict[str, Any]], dimensions: List[str], metric_keys: List[str]):
        self.fact_records = fact_records
        self.dimensions = dimensions
        self.metric_keys = metric_keys

    def slice_and_dice(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        filtered = []
        for record in self.fact_records:
            match = True
            for dim, expected in filters.items():
                if record.get(dim) != expected:
                    match = False
                    break
            if match:
                filtered.append(record)
        return filtered

    def aggregate_by(self, group_by_dimensions: List[str]) -> List[Dict[str, Any]]:
        groups = defaultdict(lambda: {k: 0.0 for k in self.metric_keys})
        counts = defaultdict(int)

        for record in self.fact_records:
            key_tuple = tuple(record.get(dim) for dim in group_by_dimensions)
            for m in self.metric_keys:
                groups[key_tuple][m] += float(record.get(m, 0.0))
            counts[key_tuple] += 1

        result = []
        for key_tuple, metric_sums in groups.items():
            entry = {dim: key_tuple[i] for i, dim in enumerate(group_by_dimensions)}
            for m, total_val in metric_sums.items():
                entry[f"total_{m}"] = round(total_val, 2)
                entry[f"avg_{m}"] = round(total_val / max(1, counts[key_tuple]), 2)
            entry["record_count"] = counts[key_tuple]
            result.append(entry)

        return sorted(result, key=lambda x: x.get(f"total_{self.metric_keys[0]}", 0), reverse=True)
""")

    # 3. backend/app/domain_services/sales_territory_manager.py
    write_file("backend/app/domain_services/sales_territory_manager.py", """from typing import Any, Dict, List, Optional, Tuple

class SalesTerritory:
    def __init__(self, territory_id: str, name: str, region: str, countries: List[str], industries: List[str], assigned_reps: List[str]):
        self.territory_id = territory_id
        self.name = name
        self.region = region
        self.countries = countries
        self.industries = industries
        self.assigned_reps = assigned_reps

    def matches(self, company_country: str, company_industry: str) -> bool:
        country_match = (not self.countries) or (company_country.upper() in [c.upper() for c in self.countries])
        industry_match = (not self.industries) or (company_industry.lower() in [i.lower() for i in self.industries])
        return country_match and industry_match

class SalesTerritoryManager:
    def __init__(self, territories: List[SalesTerritory]):
        self.territories = territories

    def assign_company_to_territory(self, company: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        country = company.get("country", "")
        industry = company.get("industry", "")

        for t in self.territories:
            if t.matches(country, industry):
                return {
                    "territory_id": t.territory_id,
                    "territory_name": t.name,
                    "region": t.region,
                    "assigned_reps": t.assigned_reps
                }

        return None
""")

    # 4. backend/app/domain_services/event_stream_processor.py
    write_file("backend/app/domain_services/event_stream_processor.py", """import json
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

class CRMEventEnvelope:
    def __init__(self, event_type: str, tenant_id: str, payload: Dict[str, Any], actor_id: Optional[str] = None):
        self.event_id = f"evt_{int(datetime.now(timezone.utc).timestamp() * 1000)}"
        self.event_type = event_type
        self.tenant_id = tenant_id
        self.payload = payload
        self.actor_id = actor_id
        self.timestamp = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "tenant_id": self.tenant_id,
            "actor_id": self.actor_id,
            "timestamp": self.timestamp,
            "payload": self.payload
        }

class EventStreamProcessor:
    def __init__(self):
        self._handlers = {}
        self._event_journal = []

    def subscribe(self, event_type: str, handler: Callable[[CRMEventEnvelope], Any]):
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    async def publish(self, event: CRMEventEnvelope) -> List[Dict[str, Any]]:
        self._event_journal.append(event.to_dict())
        results = []

        handlers = self._handlers.get(event.event_type, [])
        for h in handlers:
            try:
                res = await h(event) if hasattr(h, "__await__") else h(event)
                results.append({"handler": getattr(h, "__name__", "anonymous"), "status": "success", "result": res})
            except Exception as e:
                results.append({"handler": getattr(h, "__name__", "anonymous"), "status": "error", "error": str(e)})

        return results
""")

    print("Created OLAP cubes, data warehouse schemas, territory manager, and event processor.")

if __name__ == '__main__':
    run()
