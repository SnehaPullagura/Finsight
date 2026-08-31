import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/marketing_creative_roi_decay_modeler.py
    write_file("backend/app/enterprise/crm_analytics/marketing_creative_roi_decay_modeler.py", """from typing import Any, Dict, List, Optional

class CreativeROIDecayModeler:
    @staticmethod
    def calculate_decay_schedule(initial_roas: float, weekly_decay_pct: float = 4.5, weeks: int = 8) -> List[Dict[str, Any]]:
        schedule = []
        current_roas = initial_roas

        for w in range(1, weeks + 1):
            schedule.append({
                "week_number": w,
                "projected_roas": round(current_roas, 2),
                "is_profitable": current_roas >= 3.0
            })
            current_roas *= (1.0 - (weekly_decay_pct / 100.0))

        return schedule
""")

    # 2. backend/app/enterprise/customer_success/health_score_expansion_cadence_engine.py
    write_file("backend/app/enterprise/customer_success/health_score_expansion_cadence_engine.py", """from typing import Any, Dict, List, Optional

class ExpansionCadenceEngine:
    @staticmethod
    def schedule_expansion_cadence(account: Dict[str, Any]) -> Dict[str, Any]:
        cname = account.get("name")
        health = int(account.get("health_score", 50))

        cadence = [
            {"day": "Day 1", "touchpoint": "CSM Executive Summary Email with Product Usage Metrics"},
            {"day": "Day 4", "touchpoint": "Invite Lead Architect to Feature Roadmap Preview"},
            {"day": "Day 8", "touchpoint": "Present Co-Termed Volume Discount Expansion Proposal"}
        ]

        return {
            "account_name": cname,
            "health_score": health,
            "recommended_cadence_steps": cadence,
            "cadence_status": "CADENCE_INITIALIZED"
        }
""")

    # 3. frontend/src/enterprise/EnterpriseCreativeROIDecayStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseCreativeROIDecayStudio.tsx", """import React, { useState } from "react";
import { TrendingDown, Target, DollarSign, CheckCircle2 } from "lucide-react";

export const EnterpriseCreativeROIDecayStudio: React.FC = () => {
  const schedule = [
    { week: "Week 1", roas: "12.4x", status: "Highly Profitable" },
    { week: "Week 2", roas: "11.8x", status: "Highly Profitable" },
    { week: "Week 4", roas: "10.6x", status: "Profitable" },
    { week: "Week 6", roas: "9.2x", status: "Profitable" },
    { week: "Week 8", roas: "7.8x", status: "Healthy / Schedule Refresh" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Target className="w-5 h-5 text-emerald-400" />
            Ad Creative ROAS Decay Trajectory Modeler
          </h3>
          <p className="text-xs text-slate-400">Projected weekly degradation of creative ROAS under constant audience frequency exposure</p>
        </div>
      </div>

      <div className="space-y-3">
        {schedule.map((s, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{s.week}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Projected ROAS: <span className="text-emerald-400 font-bold">{s.roas}</span></div>
            </div>
            <span className="text-xs text-slate-400 font-semibold">{s.status}</span>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    # 4. frontend/src/enterprise/EnterpriseExpansionCadenceStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseExpansionCadenceStudio.tsx", """import React, { useState } from "react";
import { Calendar, TrendingUp, CheckCircle2, Award } from "lucide-react";

export const EnterpriseExpansionCadenceStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Calendar className="w-5 h-5 text-emerald-400" />
            Strategic Customer Expansion Outreach Cadence
          </h3>
          <p className="text-xs text-slate-400">Multi-touch communication sequence designed for expansion sales cycles</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Cadence Active
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Touchpoint 1 (Day 1)</span>
          <div className="text-xs font-bold text-white">CSM Usage Summary</div>
          <span className="text-[10px] text-slate-400">Executive ROI Metrics Email</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Touchpoint 2 (Day 4)</span>
          <div className="text-xs font-bold text-white">Roadmap Preview</div>
          <span className="text-[10px] text-slate-400">Exclusive VIP Feature Sneak Peek</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Touchpoint 3 (Day 8)</span>
          <div className="text-xs font-bold text-white">Co-Termed Quote</div>
          <span className="text-[10px] text-emerald-400">10% Volume Discount Proposal</span>
        </div>
      </div>
    </div>
  );
};
""")

    print("Created ROI decay modeler, expansion cadence, and UI studios.")

if __name__ == '__main__':
    run()
