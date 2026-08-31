import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/executive_sales_rep_churn_retention_scoring_matrix.py
    write_file("backend/app/enterprise/crm_analytics/executive_sales_rep_churn_retention_scoring_matrix.py", """from typing import Any, Dict, List, Optional
from collections import defaultdict

class RepRetentionScoringMatrix:
    @staticmethod
    def calculate_cohort_retention(reps_cohorts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for r in reps_cohorts:
            name = r.get("rep_name")
            starting_arr = float(r.get("closed_arr_baseline", 100000.0))
            retained_arr = float(r.get("retained_arr_12m", 90000.0))

            nrr_pct = round((retained_arr / max(1.0, starting_arr)) * 100.0, 1)
            tier = "World Class NRR (> 110%)" if nrr_pct >= 110.0 else "Solid Retention (95% - 110%)" if nrr_pct >= 95.0 else "Elevated Churn (< 95%)"

            results.append({
                "rep_name": name,
                "closed_arr_baseline": starting_arr,
                "retained_arr_12m": retained_arr,
                "cohort_nrr_percentage": nrr_pct,
                "quality_tier": tier,
                "eligible_for_retention_kicker": nrr_pct >= 105.0
            })

        return sorted(results, key=lambda x: x["cohort_nrr_percentage"], reverse=True)
""")

    # 2. backend/app/enterprise/customer_success/health_score_expansion_champion_finder.py
    write_file("backend/app/enterprise/customer_success/health_score_expansion_champion_finder.py", """from typing import Any, Dict, List, Optional

class CustomerChampionIdentifier:
    @staticmethod
    def identify_promoters_and_power_users(users_activity: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        champions = []
        for u in users_activity:
            email = u.get("email")
            nps = int(u.get("nps_score", 8))
            sessions = int(u.get("sessions_monthly", 20))
            is_admin = bool(u.get("is_admin", False))

            if nps >= 9 and sessions >= 25:
                champions.append({
                    "user_email": email,
                    "account_name": u.get("account_name"),
                    "nps_rating": nps,
                    "monthly_sessions": sessions,
                    "is_account_admin": is_admin,
                    "champion_role": "Executive Sponsor" if is_admin else "Product Power Champion",
                    "advocacy_readiness": "Ready for Case Study & Expansion Co-Pitch"
                })

        return champions
""")

    # 3. frontend/src/enterprise/EnterpriseRepRetentionScoringStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseRepRetentionScoringStudio.tsx", """import React, { useState } from "react";
import { Award, TrendingUp, DollarSign, CheckCircle2 } from "lucide-react";

export const EnterpriseRepRetentionScoringStudio: React.FC = () => {
  const reps = [
    { name: "Alex Vance", baseline: "$540,000", retained: "$620,000", nrr: "114.8%", tier: "World Class" },
    { name: "Sarah Connor", baseline: "$680,000", retained: "$710,000", nrr: "104.4%", tier: "Solid Retention" },
    { name: "John Wick", baseline: "$320,000", retained: "$295,000", nrr: "92.2%", tier: "Elevated Churn" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Award className="w-5 h-5 text-emerald-400" />
            Sales Rep Customer Retention & NRR Cohort Scoring
          </h3>
          <p className="text-xs text-slate-400">12-month cohort Net Revenue Retention (NRR) achieved on closed accounts by sales rep</p>
        </div>
      </div>

      <div className="space-y-3">
        {reps.map((r, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{r.name}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Closed: {r.baseline} → 12M Retained: {r.retained}</div>
            </div>
            <div className="text-right">
              <span className="text-sm font-bold text-emerald-400">{r.nrr} NRR</span>
              <span className="text-[10px] text-slate-500 block">{r.tier}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    # 4. frontend/src/enterprise/EnterpriseChampionRadarStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseChampionRadarStudio.tsx", """import React, { useState } from "react";
import { Users, Sparkles, CheckCircle2, Award } from "lucide-react";

export const EnterpriseChampionRadarStudio: React.FC = () => {
  const champions = [
    { user: "bruce.wayne@wayne.internal", account: "Wayne Enterprises", role: "Executive Sponsor", nps: "10/10", sessions: "48 / mo" },
    { user: "tony.stark@stark.internal", account: "Stark Industries", role: "Product Power Champion", nps: "10/10", sessions: "62 / mo" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-emerald-400" />
            Customer Champion & Executive Sponsor Advocacy Radar
          </h3>
          <p className="text-xs text-slate-400">Identifies high-NPS power users and executive sponsors primed for expansion co-pitching</p>
        </div>
      </div>

      <div className="space-y-3">
        {champions.map((c, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{c.user} ({c.account})</div>
              <div className="text-[11px] text-slate-400 mt-0.5">NPS: {c.nps} • {c.sessions}</div>
            </div>
            <span className="text-xs text-emerald-400 font-semibold bg-emerald-950 border border-emerald-800 px-2.5 py-1 rounded-full">
              {c.role}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    print("Created rep retention matrix, champion finder, and UI studios.")

if __name__ == '__main__':
    run()
