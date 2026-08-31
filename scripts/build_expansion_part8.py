import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/bi_cubes/customer_360_cube.py
    write_file("backend/app/enterprise/bi_cubes/customer_360_cube.py", """from datetime import date, datetime
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
""")

    # 2. backend/app/enterprise/bi_cubes/sales_quota_attainment_cube.py
    write_file("backend/app/enterprise/bi_cubes/sales_quota_attainment_cube.py", """from typing import Any, Dict, List, Optional
from collections import defaultdict

class SalesQuotaAttainmentCube:
    @staticmethod
    def calculate_hierarchy_attainment(rep_quotas: List[Dict[str, Any]]) -> Dict[str, Any]:
        team_rollups = defaultdict(lambda: {"quota": 0.0, "closed": 0.0, "pipeline": 0.0, "reps": []})

        for r in rep_quotas:
            team = r.get("team_name", "Global Sales")
            quota = float(r.get("quota_target", 0.0))
            closed = float(r.get("closed_revenue", 0.0))
            pipe = float(r.get("open_pipeline", 0.0))

            team_rollups[team]["quota"] += quota
            team_rollups[team]["closed"] += closed
            team_rollups[team]["pipeline"] += pipe
            team_rollups[team]["reps"].append({
                "rep_id": r.get("rep_id"),
                "rep_name": r.get("rep_name"),
                "quota": quota,
                "closed": closed,
                "attainment_pct": round((closed / max(1.0, quota)) * 100.0, 1)
            })

        teams_summary = []
        company_quota = 0.0
        company_closed = 0.0
        company_pipeline = 0.0

        for tname, stats in team_rollups.items():
            t_quota = stats["quota"]
            t_closed = stats["closed"]
            t_pipe = stats["pipeline"]
            pct = round((t_closed / max(1.0, t_quota)) * 100.0, 1)
            coverage = round((t_pipe / max(1.0, t_quota - t_closed)), 2) if t_quota > t_closed else 99.0

            company_quota += t_quota
            company_closed += t_closed
            company_pipeline += t_pipe

            teams_summary.append({
                "team_name": tname,
                "total_quota": round(t_quota, 2),
                "total_closed": round(t_closed, 2),
                "open_pipeline": round(t_pipe, 2),
                "attainment_percentage": pct,
                "pipeline_coverage_ratio": coverage,
                "reps": stats["reps"]
            })

        company_attainment = round((company_closed / max(1.0, company_quota)) * 100.0, 1)

        return {
            "company_total_quota": round(company_quota, 2),
            "company_total_closed": round(company_closed, 2),
            "company_total_pipeline": round(company_pipeline, 2),
            "company_attainment_percentage": company_attainment,
            "teams": sorted(teams_summary, key=lambda x: x["total_closed"], reverse=True)
        }
""")

    # 3. backend/app/enterprise/compliance/hipaa_compliance_guard.py
    write_file("backend/app/enterprise/compliance/hipaa_compliance_guard.py", """import re
from typing import Any, Dict, List, Optional

class HIPAAComplianceGuard:
    PHI_FIELD_PATTERNS = [
        r"(?i)\b(ssn|social\s*security)\b",
        r"(?i)\b(dob|date\s*of\s*birth)\b",
        r"(?i)\b(medical|diagnosis|patient|prescription|treatment|health)\b",
        r"(?i)\b(insurance|policy\s*num|medicaid|medicare)\b"
    ]

    @staticmethod
    def sanitize_phi_payload(payload: Dict[str, Any], is_authorized_medical_actor: bool = False) -> Dict[str, Any]:
        if is_authorized_medical_actor:
            return payload

        sanitized = {}
        for k, v in payload.items():
            is_phi = any(re.search(pat, k) for pat in HIPAAComplianceGuard.PHI_FIELD_PATTERNS)
            if is_phi and isinstance(v, str):
                # Redact PHI field
                sanitized[k] = f"[REDACTED_HIPAA_PHI::{k.upper()}]"
            elif isinstance(v, dict):
                sanitized[k] = HIPAAComplianceGuard.sanitize_phi_payload(v, is_authorized_medical_actor)
            else:
                sanitized[k] = v

        return sanitized
""")

    # 4. frontend/src/enterprise/EnterpriseCustomer360View.tsx
    write_file("frontend/src/enterprise/EnterpriseCustomer360View.tsx", """import React, { useState } from "react";
import { Building, DollarSign, Users, Award, Shield, CheckCircle2, TrendingUp, AlertCircle, Phone, Mail } from "lucide-react";

export const EnterpriseCustomer360View: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-emerald-950 border border-emerald-800 flex items-center justify-center text-emerald-400 font-bold text-lg">
            ST
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-xl font-bold text-white">Stark Industries Global</h2>
              <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-[10px] font-bold px-2 py-0.5 rounded-full uppercase">Enterprise Tier 1</span>
            </div>
            <p className="text-xs text-slate-400">Technology & Aerospace • New York, USA • 1,200 Employees</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <div className="text-right">
            <span className="text-[11px] text-slate-400 font-medium">Customer Health Score</span>
            <div className="text-xl font-bold text-emerald-400">94 / 100 (Grade A)</div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Annual Run Rate (ARR)</span>
          <div className="text-xl font-bold text-white mt-1">$450,000</div>
          <span className="text-[10px] text-emerald-400">Auto-Renews: Dec 2026</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Lifetime Value (LTV)</span>
          <div className="text-xl font-bold text-white mt-1">$1,250,000</div>
          <span className="text-[10px] text-emerald-400">3-Year Retention</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Active Support Tickets</span>
          <div className="text-xl font-bold text-white mt-1">0 Open</div>
          <span className="text-[10px] text-emerald-400">100% SLA Compliant</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Stakeholder Count</span>
          <div className="text-xl font-bold text-white mt-1">8 Key Contacts</div>
          <span className="text-[10px] text-slate-400">Executive Sponsor Aligned</span>
        </div>
      </div>
    </div>
  );
};
""")

    print("Created Customer 360 cube, quota cube, HIPAA guard, and Customer 360 UI.")

if __name__ == '__main__':
    run()
