import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/marketing_channel_elasticity_modeler.py
    write_file("backend/app/enterprise/crm_analytics/marketing_channel_elasticity_modeler.py", """from typing import Any, Dict, List, Optional

class MarketingElasticityModeler:
    @staticmethod
    def calculate_spend_elasticity(
        spend_change_pct: float,
        lead_volume_change_pct: float
    ) -> Dict[str, Any]:
        elasticity_coefficient = round(lead_volume_change_pct / max(0.01, spend_change_pct), 2)

        tier = "Elastic / Highly Scalable (> 1.0)" if elasticity_coefficient >= 1.0 else "Inelastic / Diminishing Scale (0.5 - 1.0)" if elasticity_coefficient >= 0.5 else "Highly Inelastic / Saturated (< 0.5)"

        return {
            "spend_change_percentage": spend_change_pct,
            "lead_volume_change_percentage": lead_volume_change_pct,
            "elasticity_coefficient": elasticity_coefficient,
            "channel_scale_readiness": tier,
            "is_spend_expansion_recommended": elasticity_coefficient >= 0.8
        }
""")

    # 2. backend/app/enterprise/customer_success/health_score_ai_summary_narrator.py
    write_file("backend/app/enterprise/customer_success/health_score_ai_summary_narrator.py", """from typing import Any, Dict, Optional

class HealthScoreNarrativeGenerator:
    @staticmethod
    def generate_executive_account_narrative(account: Dict[str, Any]) -> Dict[str, Any]:
        cname = account.get("name")
        health = int(account.get("health_score", 50))
        nps = int(account.get("nps", 8))
        arr = account.get("current_arr", "$100,000")

        if health >= 85:
            summary = f"{cname} is an elite champion account ({health}/100) with strong NPS ({nps}/10) and expanding ARR ({arr}). Ideal candidate for case study and advisory board."
        elif health >= 65:
            summary = f"{cname} is in stable health ({health}/100). Recommend scheduling standard quarterly business review to maintain momentum."
        else:
            summary = f"{cname} is currently at elevated risk ({health}/100). Executive outreach and dedicated technical triage recommended immediately."

        return {
            "account_name": cname,
            "health_score": health,
            "executive_summary_narrative": summary,
            "urgency": "High" if health < 65 else "Low"
        }
""")

    # 3. frontend/src/enterprise/EnterpriseChannelElasticityStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseChannelElasticityStudio.tsx", """import React, { useState } from "react";
import { Target, TrendingUp, DollarSign, CheckCircle2 } from "lucide-react";

export const EnterpriseChannelElasticityStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Target className="w-5 h-5 text-emerald-400" />
            Marketing Spend Elasticity & Channel Responsiveness
          </h3>
          <p className="text-xs text-slate-400">Elasticity coefficient quantifying lead volume expansion relative to budget increases</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          1.24x Elastic (High Growth)
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Tested Budget Lift</span>
          <div className="text-2xl font-bold text-white">+25.0%</div>
          <span className="text-[10px] text-slate-400">Quarterly Channel Test</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Lead Volume Expansion</span>
          <div className="text-2xl font-bold text-emerald-400">+31.0%</div>
          <span className="text-[10px] text-emerald-400">Above Linear Growth</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Elasticity Coefficient</span>
          <div className="text-2xl font-bold text-emerald-400">1.24x</div>
          <span className="text-[10px] text-slate-400">Recommend Budget Expansion</span>
        </div>
      </div>
    </div>
  );
};
""")

    # 4. frontend/src/enterprise/EnterpriseCSNarrativeSummaryStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseCSNarrativeSummaryStudio.tsx", """import React, { useState } from "react";
import { Sparkles, HeartPulse, CheckCircle2, MessageSquare } from "lucide-react";

export const EnterpriseCSNarrativeSummaryStudio: React.FC = () => {
  const narratives = [
    { name: "Acme Global Industries", health: 95, narrative: "Acme Global is an elite champion account (95/100) with strong NPS (10/10) and expanding ARR ($320k).", urgency: "Low" },
    { name: "Cyberdyne Systems", health: 48, narrative: "Cyberdyne Systems is at elevated risk (48/100). Executive outreach and dedicated technical triage recommended.", urgency: "High" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-emerald-400" />
            AI Prescriptive Account Health Narratives
          </h3>
          <p className="text-xs text-slate-400">Automated natural language executive briefings synthesized from telemetry and support tickets</p>
        </div>
      </div>

      <div className="space-y-3">
        {narratives.map((n, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-white">{n.name}</span>
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                n.urgency === "High" ? "bg-red-950 text-red-400 border border-red-800" : "bg-emerald-950 text-emerald-400 border border-emerald-800"
              }`}>
                {n.urgency} Urgency
              </span>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">{n.narrative}</p>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    print("Created elasticity modeler, CS narrator, and UI studios.")

if __name__ == '__main__':
    run()
