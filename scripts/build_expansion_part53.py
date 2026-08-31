import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/executive_sales_pipeline_inactivity_watchdog.py
    write_file("backend/app/enterprise/crm_analytics/executive_sales_pipeline_inactivity_watchdog.py", """from datetime import date
from typing import Any, Dict, List, Optional

class PipelineInactivityWatchdog:
    @staticmethod
    def identify_stagnant_deals(deals: List[Dict[str, Any]], max_allowed_inactivity_days: int = 14) -> List[Dict[str, Any]]:
        stagnant = []
        for d in deals:
            dname = d.get("name")
            val = float(d.get("value", 0.0))
            inactive_days = int(d.get("days_since_last_activity", 0))

            if inactive_days >= max_allowed_inactivity_days:
                stagnant.append({
                    "deal_name": dname,
                    "deal_value": val,
                    "days_inactive": inactive_days,
                    "rep_owner": d.get("owner_name", "Unassigned"),
                    "recommended_action": "DISPATCH_REENGAGEMENT_PLAYBOOK",
                    "severity": "CRITICAL" if inactive_days >= 30 else "WARNING"
                })

        return sorted(stagnant, key=lambda x: x["days_inactive"], reverse=True)
""")

    # 2. backend/app/enterprise/customer_success/health_score_executive_sponsor_matrix.py
    write_file("backend/app/enterprise/customer_success/health_score_executive_sponsor_matrix.py", """from typing import Any, Dict, List, Optional

class ExecutiveSponsorAlignmentMatrix:
    @staticmethod
    def audit_sponsor_coverage(accounts: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_enterprise_accounts = len(accounts)
        covered_accounts = [a for a in accounts if a.get("executive_sponsor_email")]
        uncovered_accounts = [a for a in accounts if not a.get("executive_sponsor_email")]

        coverage_pct = round((len(covered_accounts) / max(1, total_enterprise_accounts)) * 100.0, 1)

        return {
            "total_accounts_audited": total_enterprise_accounts,
            "sponsor_aligned_count": len(covered_accounts),
            "unaligned_count": len(uncovered_accounts),
            "sponsor_coverage_percentage": coverage_pct,
            "governance_status": "EXCELLENT_COVERAGE (> 90%)" if coverage_pct >= 90.0 else "SPONSOR_GAP_NEEDS_ACTION",
            "at_risk_unaligned_accounts": [a.get("name") for a in uncovered_accounts]
        }
""")

    # 3. frontend/src/enterprise/EnterprisePipelineWatchdogStudio.tsx
    write_file("frontend/src/enterprise/EnterprisePipelineWatchdogStudio.tsx", """import React, { useState } from "react";
import { AlertCircle, Clock, ShieldAlert, CheckCircle2 } from "lucide-react";

export const EnterprisePipelineWatchdogStudio: React.FC = () => {
  const stagnant = [
    { name: "Oscorp Holdings MSA", value: "$95,000", days: 28, rep: "John Wick", severity: "Warning" },
    { name: "Cyberdyne Systems AI Expansion", value: "$45,000", days: 34, rep: "John Wick", severity: "Critical" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Clock className="w-5 h-5 text-amber-400" />
            Deal Stagnation & Pipeline Inactivity Watchdog
          </h3>
          <p className="text-xs text-slate-400">Automated alerts for enterprise opportunities without recorded touchpoints over 14+ days</p>
        </div>
      </div>

      <div className="space-y-3">
        {stagnant.map((s, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{s.name} ({s.value})</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Owner: {s.rep} • {s.days} days with zero customer activity</div>
            </div>
            <span className={`text-xs font-bold px-2.5 py-1 rounded-full ${
              s.severity === "Critical" ? "bg-red-950 text-red-400 border border-red-800" : "bg-amber-950 text-amber-400 border border-amber-800"
            }`}>
              {s.severity}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    # 4. frontend/src/enterprise/EnterpriseSponsorAlignmentStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseSponsorAlignmentStudio.tsx", """import React, { useState } from "react";
import { Users, ShieldCheck, CheckCircle2, Award } from "lucide-react";

export const EnterpriseSponsorAlignmentStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Users className="w-5 h-5 text-emerald-400" />
            Executive Sponsor & Economic Buyer Alignment Matrix
          </h3>
          <p className="text-xs text-slate-400">Governance index ensuring every top-tier ARR account has an active VP/C-Suite sponsor</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          94.2% Sponsor Coverage
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Tier 1 Accounts Audited</span>
          <div className="text-2xl font-bold text-white">48 Accounts</div>
          <span className="text-[10px] text-slate-400">&gt; $100k ARR Cohort</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Sponsor Aligned</span>
          <div className="text-2xl font-bold text-emerald-400">45 Accounts</div>
          <span className="text-[10px] text-emerald-400">C-Level / VP Confirmed</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Sponsor Gap</span>
          <div className="text-2xl font-bold text-amber-400">3 Accounts</div>
          <span className="text-[10px] text-slate-400">CSM Outreach Assigned</span>
        </div>
      </div>
    </div>
  );
};
""")

    print("Created inactivity watchdog, sponsor alignment matrix, and UI studios.")

if __name__ == '__main__':
    run()
