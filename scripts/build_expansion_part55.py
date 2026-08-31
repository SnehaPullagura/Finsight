import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/marketing_creative_performance_attribution.py
    write_file("backend/app/enterprise/crm_analytics/marketing_creative_performance_attribution.py", """from typing import Any, Dict, List, Optional

class CreativeAttributionMatrix:
    @staticmethod
    def calculate_creative_influence(creatives: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_influenced_pipeline = sum(float(c.get("influenced_pipeline", 0.0)) for c in creatives)
        top_creative = max(creatives, key=lambda x: float(x.get("influenced_pipeline", 0.0))) if creatives else {}

        return {
            "total_influenced_pipeline": round(total_influenced_pipeline, 2),
            "top_performing_asset": top_creative.get("title"),
            "top_asset_pipeline_share_pct": round((float(top_creative.get("influenced_pipeline", 0.0)) / max(1.0, total_influenced_pipeline)) * 100.0, 1) if creatives else 0.0,
            "creative_attribution_model": "Multi-Touch Algorithmic W-Shaped Weighting"
        }
""")

    # 2. backend/app/enterprise/customer_success/health_score_expansion_governance_guard.py
    write_file("backend/app/enterprise/customer_success/health_score_expansion_governance_guard.py", """from typing import Any, Dict, List, Optional

class ExpansionGovernanceGuard:
    @staticmethod
    def validate_expansion_prerequisites(account: Dict[str, Any]) -> Dict[str, Any]:
        health = int(account.get("health_score", 50))
        open_sev1_tickets = int(account.get("open_sev1_tickets_count", 0))
        past_due_invoices = int(account.get("unpaid_invoices_count", 0))

        is_eligible = health >= 70 and open_sev1_tickets == 0 and past_due_invoices == 0

        return {
            "account_name": account.get("name"),
            "health_score": health,
            "open_sev1_tickets": open_sev1_tickets,
            "past_due_invoices": past_due_invoices,
            "is_expansion_eligible": is_eligible,
            "blocker_reason": "Sev 1 Support Ticket Pending" if open_sev1_tickets > 0 else "Unpaid Invoices Present" if past_due_invoices > 0 else "Sub-Optimal Health" if health < 70 else "None (Clear to Propose)"
        }
""")

    # 3. frontend/src/enterprise/EnterprisePipelineVelocityAttributionStudio.tsx
    write_file("frontend/src/enterprise/EnterprisePipelineVelocityAttributionStudio.tsx", """import React, { useState } from "react";
import { Zap, Target, TrendingUp, CheckCircle2 } from "lucide-react";

export const EnterprisePipelineVelocityAttributionStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Zap className="w-5 h-5 text-emerald-400" />
            Marketing Creative Pipeline Velocity Attribution
          </h3>
          <p className="text-xs text-slate-400">Multi-touch W-shaped attribution mapping interactive collateral directly to closed revenue</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          +$6.8M Influenced
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Top Converting Creative</span>
          <div className="text-2xl font-bold text-white">Interactive CPQ Tour</div>
          <span className="text-[10px] text-emerald-400">42.5% Pipeline Influence Share</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Attributed Closed ARR</span>
          <div className="text-2xl font-bold text-emerald-400">$2,890,000</div>
          <span className="text-[10px] text-slate-400">18 Enterprise Closed-Won Deals</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Attribution Model</span>
          <div className="text-2xl font-bold text-white">W-Shaped 40/40/20</div>
          <span className="text-[10px] text-slate-400">First / Mid / Opportunity Touch</span>
        </div>
      </div>
    </div>
  );
};
""")

    # 4. frontend/src/enterprise/EnterpriseExpansionGovernanceGuardStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseExpansionGovernanceGuardStudio.tsx", """import React, { useState } from "react";
import { ShieldCheck, AlertCircle, CheckCircle2, DollarSign } from "lucide-react";

export const EnterpriseExpansionGovernanceGuardStudio: React.FC = () => {
  const audits = [
    { account: "Wayne Enterprises", health: 94, tickets: 0, invoices: 0, status: "Clear to Propose" },
    { account: "Stark Industries", health: 88, tickets: 0, invoices: 0, status: "Clear to Propose" },
    { account: "Cyberdyne Systems", health: 62, tickets: 1, invoices: 0, status: "Blocked (Sev 1 Open)" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            Customer Expansion Governance & Prerequisite Guard
          </h3>
          <p className="text-xs text-slate-400">Automated policy checks preventing upsell outreach during open Sev-1 outages or billing disputes</p>
        </div>
      </div>

      <div className="space-y-3">
        {audits.map((a, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{a.account}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Health: {a.health} • Open Tickets: {a.tickets} • Overdue Invoices: {a.invoices}</div>
            </div>
            <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${
              a.status === "Clear to Propose" ? "bg-emerald-950 text-emerald-400 border border-emerald-800" : "bg-red-950 text-red-400 border border-red-800"
            }`}>
              {a.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    print("Created creative attribution, governance guard, and UI studios.")

if __name__ == '__main__':
    run()
