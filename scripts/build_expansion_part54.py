import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/marketing_creative_fatigue_alert_queue.py
    write_file("backend/app/enterprise/crm_analytics/marketing_creative_fatigue_alert_queue.py", """from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class CreativeFatigueAlertQueue:
    @staticmethod
    def queue_fatigued_creatives(fatigued_ads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        alerts = []
        for ad in fatigued_ads:
            alerts.append({
                "alert_id": f"cfa_{int(datetime.now(timezone.utc).timestamp() * 1000)}",
                "creative_id": ad.get("id"),
                "creative_title": ad.get("title"),
                "current_cpa": ad.get("cpa"),
                "cpa_inflation_pct": ad.get("cpa_inflation_pct"),
                "dispatched_at": datetime.now(timezone.utc).isoformat(),
                "action_status": "AUTO_PAUSED_AND_REPLACED"
            })
        return alerts
""")

    # 2. backend/app/enterprise/customer_success/health_score_expansion_target_modeler.py
    write_file("backend/app/enterprise/customer_success/health_score_expansion_target_modeler.py", """from typing import Any, Dict, List, Optional

class CSExpansionTargetModeler:
    @staticmethod
    def calculate_portfolio_expansion_runway(accounts: List[Dict[str, Any]], target_expansion_rate_pct: float = 25.0) -> Dict[str, Any]:
        total_base_arr = sum(float(a.get("current_arr", 0.0)) for a in accounts)
        target_expansion_arr = round(total_base_arr * (target_expansion_rate_pct / 100.0), 2)
        projected_total_ending_arr = round(total_base_arr + target_expansion_arr, 2)

        return {
            "total_accounts_count": len(accounts),
            "portfolio_base_arr": total_base_arr,
            "target_expansion_rate_pct": target_expansion_rate_pct,
            "projected_net_expansion_dollars": target_expansion_arr,
            "projected_ending_arr": projected_total_ending_arr,
            "expansion_health": "Target Achievable" if len(accounts) >= 10 else "High Concentration Risk"
        }
""")

    # 3. frontend/src/enterprise/EnterpriseCreativeAlertQueueStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseCreativeAlertQueueStudio.tsx", """import React, { useState } from "react";
import { AlertTriangle, RefreshCw, CheckCircle2, DollarSign } from "lucide-react";

export const EnterpriseCreativeAlertQueueStudio: React.FC = () => {
  const alerts = [
    { title: "Legacy Migration Webinar Ad", cpa: "$142.50", inflation: "+54.2%", status: "Auto-Paused & Replaced" },
    { title: "Generic Enterprise CPQ Banner", cpa: "$98.00", inflation: "+38.4%", status: "Queued for Refresh" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-amber-400" />
            Ad Fatigue Real-Time Queue & Auto-Pause Guard
          </h3>
          <p className="text-xs text-slate-400">Automated budget protection pausing exhausted creatives with CPA spikes</p>
        </div>
      </div>

      <div className="space-y-3">
        {alerts.map((a, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{a.title}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Current CPA: {a.cpa} • CPA Spike: <span className="text-amber-400 font-bold">{a.inflation}</span></div>
            </div>
            <span className="text-xs text-emerald-400 font-semibold bg-emerald-950 border border-emerald-800 px-2.5 py-1 rounded-full">
              {a.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    # 4. frontend/src/enterprise/EnterpriseExpansionTargetModelerStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseExpansionTargetModelerStudio.tsx", """import React, { useState } from "react";
import { Target, TrendingUp, DollarSign, Award, CheckCircle2 } from "lucide-react";

export const EnterpriseExpansionTargetModelerStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Target className="w-5 h-5 text-emerald-400" />
            Portfolio ARR Expansion Runway & Target Modeler
          </h3>
          <p className="text-xs text-slate-400">Simulate 12-month net expansion runway across installed enterprise account cohorts</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          +25.0% Expansion Target
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Installed Base Baseline</span>
          <div className="text-2xl font-bold text-white">$14.2M ARR</div>
          <span className="text-[10px] text-slate-400">128 Enterprise Accounts</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Target Expansion Net</span>
          <div className="text-2xl font-bold text-emerald-400">+$3.55M ARR</div>
          <span className="text-[10px] text-emerald-400">Seat Upsell & Advanced Modules</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Projected Ending ARR</span>
          <div className="text-2xl font-bold text-white">$17.75M ARR</div>
          <span className="text-[10px] text-emerald-400">125% Net Expansion Pace</span>
        </div>
      </div>
    </div>
  );
};
""")

    print("Created fatigue alert queue, expansion target modeler, and UI studios.")

if __name__ == '__main__':
    run()
