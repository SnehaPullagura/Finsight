import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/marketing_creative_decay_lifecycle.py
    write_file("backend/app/enterprise/crm_analytics/marketing_creative_decay_lifecycle.py", """from typing import Any, Dict, List, Optional

class CreativeDecayLifecycleModeler:
    @staticmethod
    def calculate_creative_lifecycle(days_active: int, initial_ctr: float, current_ctr: float) -> Dict[str, Any]:
        fatigue_pct = round(((initial_ctr - current_ctr) / max(0.01, initial_ctr)) * 100.0, 1)

        stage = "Peak Performance (< 14d)" if days_active <= 14 else "Maturity / High Volume (14-45d)" if days_active <= 45 and fatigue_pct < 20 else "Fatigued / Replacement Needed (> 45d)"

        return {
            "days_active": days_active,
            "initial_ctr": initial_ctr,
            "current_ctr": current_ctr,
            "fatigue_percentage": fatigue_pct,
            "lifecycle_stage": stage,
            "requires_refresh": fatigue_pct >= 25.0 or days_active > 60
        }
""")

    # 2. backend/app/enterprise/customer_success/health_score_expansion_pipeline_generator.py
    write_file("backend/app/enterprise/customer_success/health_score_expansion_pipeline_generator.py", """from typing import Any, Dict, List, Optional

class ExpansionPipelineGenerator:
    @staticmethod
    def generate_expansion_deals(expansion_candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        deals = []
        for cand in expansion_candidates:
            cid = cand.get("account_id")
            cname = cand.get("account_name")
            expansion_arr = float(cand.get("projected_expansion_arr", 25000.0))

            deals.append({
                "deal_name": f"{cname} — Expansion & Add-On License",
                "account_id": cid,
                "pipeline_stage": "Discovery",
                "deal_value": expansion_arr,
                "probability": 75,
                "expected_close_in_days": 30,
                "deal_type": "Existing Customer Expansion",
                "lead_source": "Automated CS Health Signal"
            })

        return deals
""")

    # 3. frontend/src/enterprise/EnterpriseCreativeLifecycleStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseCreativeLifecycleStudio.tsx", """import React, { useState } from "react";
import { RefreshCw, Target, TrendingDown, CheckCircle2 } from "lucide-react";

export const EnterpriseCreativeLifecycleStudio: React.FC = () => {
  const creatives = [
    { name: "Executive CPQ Video Tour", days: 12, ctr: "3.8%", fatigue: "0%", stage: "Peak Performance" },
    { name: "Multi-Tenant Whitepaper Ad", days: 38, ctr: "2.9%", fatigue: "-8.5%", stage: "Maturity" },
    { name: "Legacy Migration Webinar", days: 54, ctr: "1.4%", fatigue: "-38.2%", stage: "Fatigued" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <RefreshCw className="w-5 h-5 text-emerald-400" />
            Ad Creative Lifecycle & Fatigue Staging Studio
          </h3>
          <p className="text-xs text-slate-400">Automated tracking of creative age, performance decay, and variant retirement</p>
        </div>
      </div>

      <div className="space-y-3">
        {creatives.map((c, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{c.name}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">{c.days} days active • Current CTR: {c.ctr} • Decay: {c.fatigue}</div>
            </div>
            <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${
              c.stage === "Peak Performance" ? "bg-emerald-950 text-emerald-400 border border-emerald-800" :
              c.stage === "Maturity" ? "bg-blue-950 text-blue-400 border border-blue-800" : "bg-amber-950 text-amber-400 border border-amber-800"
            }`}>
              {c.stage}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    # 4. frontend/src/enterprise/EnterpriseExpansionPipelineStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseExpansionPipelineStudio.tsx", """import React, { useState } from "react";
import { TrendingUp, Plus, DollarSign, CheckCircle2 } from "lucide-react";

export const EnterpriseExpansionPipelineStudio: React.FC = () => {
  const deals = [
    { title: "Wayne Enterprises — Expansion & Add-On", value: "$62,500", prob: "75%", stage: "Discovery" },
    { title: "Stark Industries — Additional 50 Seats", value: "$45,000", prob: "80%", stage: "Scoping" },
    { title: "Cyberdyne Systems — AI Copilot Expansion", value: "$23,750", prob: "70%", stage: "Discovery" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-emerald-400" />
            Automated Customer Success Expansion Pipeline
          </h3>
          <p className="text-xs text-slate-400">Auto-generated expansion pipeline opportunities triggered by telemetry thresholds</p>
        </div>
        <button className="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-500 text-white px-3 py-1.5 rounded-lg text-xs font-semibold shadow transition-colors">
          <Plus className="w-4 h-4" />
          Sync to CRM
        </button>
      </div>

      <div className="space-y-3">
        {deals.map((d, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{d.title}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Stage: {d.stage} • Probability: {d.prob}</div>
            </div>
            <div className="text-right">
              <span className="text-sm font-bold text-emerald-400">{d.value}</span>
              <span className="text-[10px] text-slate-500 block">Expansion ARR</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    print("Created creative lifecycle, expansion pipeline generator, and UI studios.")

if __name__ == '__main__':
    run()
