import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/executive_sales_capacity_planner.py
    write_file("backend/app/enterprise/crm_analytics/executive_sales_capacity_planner.py", """from typing import Any, Dict, List, Optional

class SalesCapacityPlanner:
    @staticmethod
    def plan_hiring_capacity(
        annual_revenue_target: float,
        ramped_rep_annual_quota: float,
        average_ramp_months: int,
        expected_annual_attrition_pct: float = 15.0
    ) -> Dict[str, Any]:
        base_reps_needed = annual_revenue_target / max(1.0, ramped_rep_annual_quota)
        attrition_buffer = base_reps_needed * (expected_annual_attrition_pct / 100.0)
        ramp_lag_multiplier = 1.0 + (average_ramp_months / 12.0)

        total_headcount_target = round((base_reps_needed + attrition_buffer) * ramp_lag_multiplier, 1)

        return {
            "annual_revenue_target": annual_revenue_target,
            "annual_quota_per_rep": ramped_rep_annual_quota,
            "base_ramped_reps_required": round(base_reps_needed, 1),
            "attrition_headcount_buffer": round(attrition_buffer, 1),
            "total_headcount_to_hire": total_headcount_target,
            "quarterly_hiring_cadence": [
                {"quarter": "Q1", "target_hires": int(total_headcount_target * 0.4)},
                {"quarter": "Q2", "target_hires": int(total_headcount_target * 0.3)},
                {"quarter": "Q3", "target_hires": int(total_headcount_target * 0.2)},
                {"quarter": "Q4", "target_hires": int(total_headcount_target * 0.1)}
            ]
        }
""")

    # 2. backend/app/enterprise/crm_analytics/marketing_mql_aging_velocity.py
    write_file("backend/app/enterprise/crm_analytics/marketing_mql_aging_velocity.py", """from typing import Any, Dict, List, Optional

class MQLAgingVelocityAnalyzer:
    @staticmethod
    def calculate_mql_decay(mql_leads: List[Dict[str, Any]]) -> Dict[str, Any]:
        buckets = {"sub_24h": 0, "day_1_to_3": 0, "day_3_to_7": 0, "stale_7d_plus": 0}
        total = len(mql_leads)

        for l in mql_leads:
            hours = float(l.get("hours_since_qualification", 0.0))
            if hours <= 24:
                buckets["sub_24h"] += 1
            elif hours <= 72:
                buckets["day_1_to_3"] += 1
            elif hours <= 168:
                buckets["day_3_to_7"] += 1
            else:
                buckets["stale_7d_plus"] += 1

        pct_sub_24h = round((buckets["sub_24h"] / max(1, total)) * 100.0, 1)

        return {
            "total_mql_leads": total,
            "aging_buckets": buckets,
            "pct_contacted_under_24h": pct_sub_24h,
            "velocity_rating": "Elite Response Speed" if pct_sub_24h >= 80.0 else "Acceptable" if pct_sub_24h >= 50.0 else "High SDR Friction"
        }
""")

    # 3. frontend/src/enterprise/EnterpriseSalesCapacityStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseSalesCapacityStudio.tsx", """import React, { useState } from "react";
import { Users, TrendingUp, DollarSign, Calendar, Award } from "lucide-react";

export const EnterpriseSalesCapacityStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Users className="w-5 h-5 text-emerald-400" />
            Sales Headcount & Capacity Planning Model
          </h3>
          <p className="text-xs text-slate-400">Headcount modeling incorporating ramp time, sales cycle lag, and historical rep attrition</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Plan Approved
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">ARR Growth Target</span>
          <div className="text-2xl font-bold text-white">$15.0M</div>
          <span className="text-[10px] text-emerald-400">+100% YoY Target</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Ramped Quota per Rep</span>
          <div className="text-2xl font-bold text-white">$1,200,000</div>
          <span className="text-[10px] text-slate-400">4.5 Mo Average Ramp</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Total AE Hires Needed</span>
          <div className="text-2xl font-bold text-emerald-400">18 Reps</div>
          <span className="text-[10px] text-slate-400">Includes 15% Attrition Buffer</span>
        </div>
      </div>
    </div>
  );
};
""")

    # 4. frontend/src/enterprise/EnterpriseMQLAgingVelocityStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseMQLAgingVelocityStudio.tsx", """import React, { useState } from "react";
import { Clock, Zap, CheckCircle2, TrendingUp } from "lucide-react";

export const EnterpriseMQLAgingVelocityStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Zap className="w-5 h-5 text-emerald-400" />
            MQL Inbound Speed-to-Lead Velocity
          </h3>
          <p className="text-xs text-slate-400">Distribution of inbound lead outreach response times across SDR team</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          92.4% Under 24 Hours
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">&lt; 24 Hours (Fast Track)</span>
          <div className="text-xl font-bold text-emerald-400">450 Leads</div>
          <span className="text-[10px] text-emerald-400">92.4% of Total Inbound</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">1 - 3 Days</span>
          <div className="text-xl font-bold text-white">28 Leads</div>
          <span className="text-[10px] text-slate-400">5.7% of Inbound</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">3 - 7 Days</span>
          <div className="text-xl font-bold text-white">7 Leads</div>
          <span className="text-[10px] text-slate-400">1.4% of Inbound</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">&gt; 7 Days (Stale)</span>
          <div className="text-xl font-bold text-slate-500">2 Leads</div>
          <span className="text-[10px] text-slate-500">0.5%</span>
        </div>
      </div>
    </div>
  );
};
""")

    print("Created capacity planner, MQL aging analyzer, and UI studios.")

if __name__ == '__main__':
    run()
