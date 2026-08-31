import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/executive_sales_rep_churn_impact.py
    write_file("backend/app/enterprise/crm_analytics/executive_sales_rep_churn_impact.py", """from typing import Any, Dict, List, Optional
from collections import defaultdict

class RepChurnImpactModeler:
    @staticmethod
    def calculate_rep_attributed_churn(accounts_churned: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        rep_churn_map = defaultdict(lambda: {"lost_arr": 0.0, "accounts_count": 0})

        for acc in accounts_churned:
            rep = acc.get("closing_rep_name", "Unassigned")
            arr = float(acc.get("churned_arr", 0.0))
            rep_churn_map[rep]["lost_arr"] += arr
            rep_churn_map[rep]["accounts_count"] += 1

        results = []
        for rep, data in rep_churn_map.items():
            results.append({
                "rep_name": rep,
                "total_lost_arr": round(data["lost_arr"], 2),
                "churned_accounts_count": data["accounts_count"],
                "requires_onboarding_enablement": data["accounts_count"] >= 3
            })

        return sorted(results, key=lambda x: x["total_lost_arr"], reverse=True)
""")

    # 2. backend/app/enterprise/crm_analytics/marketing_creative_fatigue_detector.py
    write_file("backend/app/enterprise/crm_analytics/marketing_creative_fatigue_detector.py", """from typing import Any, Dict, List, Optional

class AdCreativeFatigueDetector:
    @staticmethod
    def evaluate_creative_fatigue(ad_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        if len(ad_history) < 2:
            return {"status": "insufficient_history"}

        ctr_initial = float(ad_history[0].get("ctr_pct", 2.5))
        ctr_current = float(ad_history[-1].get("ctr_pct", 2.5))
        cpa_initial = float(ad_history[0].get("cpa", 50.0))
        cpa_current = float(ad_history[-1].get("cpa", 50.0))

        ctr_drop_pct = round(((ctr_initial - ctr_current) / max(0.01, ctr_initial)) * 100.0, 1)
        cpa_increase_pct = round(((cpa_current - cpa_initial) / max(1.0, cpa_initial)) * 100.0, 1)

        is_fatigued = ctr_drop_pct >= 25.0 or cpa_increase_pct >= 30.0

        return {
            "initial_ctr": ctr_initial,
            "current_ctr": ctr_current,
            "ctr_drop_percentage": ctr_drop_pct,
            "cpa_increase_percentage": cpa_increase_pct,
            "is_creative_fatigued": is_fatigued,
            "action": "REFRESH_AD_CREATIVE_VARIANTS" if is_fatigued else "MAINTAIN_CURRENT_ROTATION"
        }
""")

    # 3. frontend/src/enterprise/EnterpriseCreativeFatigueRadar.tsx
    write_file("frontend/src/enterprise/EnterpriseCreativeFatigueRadar.tsx", """import React, { useState } from "react";
import { AlertTriangle, RefreshCw, TrendingDown, Target, CheckCircle2 } from "lucide-react";

export const EnterpriseCreativeFatigueRadar: React.FC = () => {
  const ads = [
    { title: "LinkedIn B2B CPQ Interactive Demo Ad", ctrDrop: "-34.2% CTR", cpaRise: "+41.5% CPA", status: "Fatigued (Action Needed)" },
    { title: "Google Search: Enterprise CRM Alternative", ctrDrop: "-4.1% CTR", cpaRise: "+1.2% CPA", status: "High Efficiency" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Target className="w-5 h-5 text-emerald-400" />
            Ad Creative Fatigue & CPA Decay Radar
          </h3>
          <p className="text-xs text-slate-400">Automated detection of declining CTRs and rising customer acquisition costs</p>
        </div>
      </div>

      <div className="space-y-3">
        {ads.map((ad, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{ad.title}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">{ad.ctrDrop} • {ad.cpaRise}</div>
            </div>
            <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${
              ad.status.includes("Fatigued") ? "bg-amber-950 text-amber-400 border border-amber-800" : "bg-emerald-950 text-emerald-400 border border-emerald-800"
            }`}>
              {ad.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    # 4. frontend/src/enterprise/EnterpriseCSInterventionWorkflow.tsx
    write_file("frontend/src/enterprise/EnterpriseCSInterventionWorkflow.tsx", """import React, { useState } from "react";
import { Play, CheckCircle2, Shield, HeartPulse, ArrowRight } from "lucide-react";

export const EnterpriseCSInterventionWorkflow: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <HeartPulse className="w-5 h-5 text-emerald-400" />
            Customer Success Escalation & Intervention Workflow
          </h3>
          <p className="text-xs text-slate-400">Automated triage routing and recovery milestone tracking</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          CS Workflow Active
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Step 1: Automated Detection</span>
          <div className="text-xs font-bold text-white">Telemetry Risk Triggered</div>
          <span className="text-[10px] text-emerald-400">&lt; 15% DAU/MAU</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Step 2: Executive Alert</span>
          <div className="text-xs font-bold text-white">Slack & Email Notification</div>
          <span className="text-[10px] text-emerald-400">Assigned Senior CSM</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Step 3: Recovery Sprint</span>
          <div className="text-xs font-bold text-white">Mutual Success Plan</div>
          <span className="text-[10px] text-emerald-400">Target: 85+ Health</span>
        </div>
      </div>
    </div>
  );
};
""")

    print("Created rep churn modeler, fatigue detector, and UI components.")

if __name__ == '__main__':
    run()
