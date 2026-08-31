import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/marketing_cac_by_tier_modeler.py
    write_file("backend/app/enterprise/crm_analytics/marketing_cac_by_tier_modeler.py", """from typing import Any, Dict, List, Optional

class TieredCACModeler:
    @staticmethod
    def calculate_tier_payback_metrics(
        enterprise_cac: float,
        midmarket_cac: float,
        smb_cac: float,
        enterprise_arpu: float,
        midmarket_arpu: float,
        smb_arpu: float,
        gross_margin_pct: float = 80.0
    ) -> Dict[str, Any]:
        margin = gross_margin_pct / 100.0

        ent_payback = round(enterprise_cac / max(1.0, enterprise_arpu * margin), 1)
        mid_payback = round(midmarket_cac / max(1.0, midmarket_arpu * margin), 1)
        smb_payback = round(smb_cac / max(1.0, smb_arpu * margin), 1)

        return {
            "enterprise": {"cac": enterprise_cac, "arpu": enterprise_arpu, "payback_months": ent_payback},
            "mid_market": {"cac": midmarket_cac, "arpu": midmarket_arpu, "payback_months": mid_payback},
            "smb": {"cac": smb_cac, "arpu": smb_arpu, "payback_months": smb_payback},
            "blended_average_payback_months": round((ent_payback + mid_payback + smb_payback) / 3.0, 1)
        }
""")

    # 2. backend/app/enterprise/crm_analytics/sales_pipeline_decay_analyzer.py
    write_file("backend/app/enterprise/crm_analytics/sales_pipeline_decay_analyzer.py", """from datetime import date, timedelta
from typing import Any, Dict, List, Optional

class SalesPipelineDecayAnalyzer:
    @staticmethod
    def calculate_opportunity_decay_rate(
        deal: Dict[str, Any],
        days_inactive: int,
        half_life_days: float = 30.0
    ) -> Dict[str, Any]:
        val = float(deal.get("value", 0.0))
        prob = float(deal.get("probability", 50.0))

        # Exponential probability decay: P(t) = P0 * (0.5 ^ (t / half_life))
        decay_factor = 0.5 ** (days_inactive / float(half_life_days))
        decayed_probability = round(prob * decay_factor, 1)
        decayed_weighted_value = round(val * (decayed_probability / 100.0), 2)

        return {
            "deal_id": deal.get("id"),
            "deal_name": deal.get("name"),
            "original_probability": prob,
            "days_inactive": days_inactive,
            "decayed_probability": decayed_probability,
            "decayed_weighted_value": decayed_weighted_value,
            "is_heavily_decayed": decayed_probability < (prob * 0.5)
        }
""")

    # 3. backend/app/enterprise/customer_success/csat_response_trend_analyzer.py
    write_file("backend/app/enterprise/customer_success/csat_response_trend_analyzer.py", """from typing import Any, Dict, List, Optional

class CSATResponseTrendAnalyzer:
    @staticmethod
    def calculate_csat_trend_momentum(monthly_ratings: List[List[int]]) -> Dict[str, Any]:
        monthly_scores = []
        for ratings in monthly_ratings:
            if not ratings:
                monthly_scores.append(0.0)
                continue
            positive = sum(1 for r in ratings if r >= 4)
            pct = round((positive / float(len(ratings))) * 100.0, 1)
            monthly_scores.append(pct)

        trend_delta = round(monthly_scores[-1] - monthly_scores[0], 1) if len(monthly_scores) >= 2 else 0.0

        return {
            "monthly_csat_scores": monthly_scores,
            "current_csat_percentage": monthly_scores[-1] if monthly_scores else 0.0,
            "quarterly_trend_delta": trend_delta,
            "momentum": "Positive Growth" if trend_delta > 2.0 else "Declining" if trend_delta < -2.0 else "Stable"
        }
""")

    # 4. frontend/src/enterprise/EnterprisePipelineDecayRadar.tsx
    write_file("frontend/src/enterprise/EnterprisePipelineDecayRadar.tsx", """import React, { useState } from "react";
import { AlertTriangle, Clock, TrendingDown, CheckCircle2 } from "lucide-react";

export const EnterprisePipelineDecayRadar: React.FC = () => {
  const decayedDeals = [
    { name: "Oscorp Systems Infrastructure", initialProb: "80%", decayedProb: "38%", daysQuiet: 45, impact: "-$54,600" },
    { name: "Cyberdyne Security License", initialProb: "60%", decayedProb: "35%", daysQuiet: 32, impact: "-$23,750" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <TrendingDown className="w-5 h-5 text-amber-400" />
            Pipeline Probability Decay & Inactivity Radar
          </h3>
          <p className="text-xs text-slate-400">Exponential probability decay modeling based on days without customer touchpoints</p>
        </div>
      </div>

      <div className="space-y-3">
        {decayedDeals.map((d, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{d.name}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">
                Initial: {d.initialProb} → Decayed: <span className="text-amber-400 font-bold">{d.decayedProb}</span> ({d.daysQuiet} days quiet)
              </div>
            </div>
            <div className="text-right">
              <span className="text-[10px] text-slate-500 uppercase font-semibold">Weighted Pipeline Loss</span>
              <div className="text-xs font-bold text-red-400">{d.impact}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    # 5. frontend/src/enterprise/EnterpriseCSATTrendsDashboard.tsx
    write_file("frontend/src/enterprise/EnterpriseCSATTrendsDashboard.tsx", """import React, { useState } from "react";
import { Smile, TrendingUp, CheckCircle2, Award } from "lucide-react";

export const EnterpriseCSATTrendsDashboard: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Smile className="w-5 h-5 text-emerald-400" />
            Customer Satisfaction (CSAT) Trajectory Dashboard
          </h3>
          <p className="text-xs text-slate-400">Quarterly post-support ticket CSAT rating distribution and trend momentum</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          96.4% CSAT (Top Decile)
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Overall CSAT</span>
          <div className="text-2xl font-bold text-emerald-400">96.4%</div>
          <span className="text-[10px] text-slate-400">↑ +2.1% MoM Improvement</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">First Contact Resolution</span>
          <div className="text-2xl font-bold text-white">88.5%</div>
          <span className="text-[10px] text-emerald-400">Target: 80%+</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Avg Resolution Time</span>
          <div className="text-2xl font-bold text-white">2.4 Hours</div>
          <span className="text-[10px] text-emerald-400">100% SLA Compliant</span>
        </div>
      </div>
    </div>
  );
};
""")

    print("Created tiered CAC, decay analyzer, CSAT trend, and UI dashboards.")

if __name__ == '__main__':
    run()
