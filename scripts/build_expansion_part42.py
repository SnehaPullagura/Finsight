import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/marketing_channel_diminishing_returns.py
    write_file("backend/app/enterprise/crm_analytics/marketing_channel_diminishing_returns.py", """import math
from typing import Any, Dict, List, Optional

class MarketingDiminishingReturnsModeler:
    @staticmethod
    def calculate_marginal_cac(current_spend: float, marginal_spend_increase: float, saturation_ceiling: float = 100000.0) -> Dict[str, Any]:
        # Logarithmic saturation model
        def customers_from_spend(spend):
            return saturation_ceiling * (1.0 - math.exp(-spend / max(1.0, saturation_ceiling)))

        base_customers = customers_from_spend(current_spend)
        incremental_customers = customers_from_spend(current_spend + marginal_spend_increase)
        new_customers_added = max(0.01, incremental_customers - base_customers)

        marginal_cac = round(marginal_spend_increase / new_customers_added, 2)
        base_cac = round(current_spend / max(0.01, base_customers), 2)
        cac_inflation_pct = round(((marginal_cac - base_cac) / max(1.0, base_cac)) * 100.0, 1)

        return {
            "current_monthly_spend": current_spend,
            "incremental_spend_tested": marginal_spend_increase,
            "baseline_cac": base_cac,
            "marginal_incremental_cac": marginal_cac,
            "cac_inflation_percentage": cac_inflation_pct,
            "saturation_status": "Near Saturation (High CAC Inflation)" if cac_inflation_pct >= 50.0 else "Healthy Scale" if cac_inflation_pct >= 15.0 else "Underspent / High Margin"
        }
""")

    # 2. backend/app/enterprise/customer_success/health_score_expansion_propensity.py
    write_file("backend/app/enterprise/customer_success/health_score_expansion_propensity.py", """from typing import Any, Dict, List, Optional

class ExpansionPropensityScorer:
    @staticmethod
    def score_account_expansion(account: Dict[str, Any]) -> Dict[str, Any]:
        health = int(account.get("health_score", 50))
        nps = int(account.get("nps", 8))
        seat_util = float(account.get("seat_utilization_pct", 75.0))
        feature_depth = int(account.get("features_adopted_count", 5))

        # Composite score
        propensity = (health * 0.4) + (seat_util * 0.3) + (nps * 2.0) + (feature_depth * 2.0)
        final_score = min(100, int(propensity))

        tier = "High Expansion Propensity" if final_score >= 80 else "Moderate" if final_score >= 60 else "Low Readiness"

        return {
            "account_id": account.get("id"),
            "account_name": account.get("name"),
            "expansion_propensity_score": final_score,
            "readiness_tier": tier,
            "recommended_play": "Introduce Advanced Analytics & Add-On Modules" if final_score >= 80 else "Drive Daily User Adoption"
        }
""")

    # 3. frontend/src/enterprise/EnterpriseDiminishingReturnsStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseDiminishingReturnsStudio.tsx", """import React, { useState } from "react";
import { TrendingDown, DollarSign, Target, CheckCircle2 } from "lucide-react";

export const EnterpriseDiminishingReturnsStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Target className="w-5 h-5 text-emerald-400" />
            Ad Spend Diminishing Returns & Marginal CAC Saturation
          </h3>
          <p className="text-xs text-slate-400">Logarithmic channel saturation curve identifying marginal acquisition cost inflation</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Healthy Scale Band
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Current Blended CAC</span>
          <div className="text-2xl font-bold text-white">$2,450</div>
          <span className="text-[10px] text-slate-400">At $50k / Mo Spend</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Marginal Incremental CAC</span>
          <div className="text-2xl font-bold text-emerald-400">$2,980</div>
          <span className="text-[10px] text-emerald-400">+$20k Incremental Budget</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">CAC Inflation</span>
          <div className="text-2xl font-bold text-white">+21.6%</div>
          <span className="text-[10px] text-emerald-400">Optimal Scale Frontier</span>
        </div>
      </div>
    </div>
  );
};
""")

    # 4. frontend/src/enterprise/EnterpriseExpansionPropensityStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseExpansionPropensityStudio.tsx", """import React, { useState } from "react";
import { TrendingUp, Users, DollarSign, Award, CheckCircle2 } from "lucide-react";

export const EnterpriseExpansionPropensityStudio: React.FC = () => {
  const accounts = [
    { name: "Wayne Enterprises", score: 94, arr: "$250,000", play: "Advanced Security Addon", tier: "High Propensity" },
    { name: "Stark Industries", score: 89, arr: "$180,000", play: "Additional 50 Seats", tier: "High Propensity" },
    { name: "Oscorp Holdings", score: 72, arr: "$95,000", play: "AI Copilot Module", tier: "Moderate" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-emerald-400" />
            Account Upsell & Expansion Propensity Matrix
          </h3>
          <p className="text-xs text-slate-400">Multi-variate algorithmic readiness scoring for seat and feature expansion</p>
        </div>
      </div>

      <div className="space-y-3">
        {accounts.map((a, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{a.name}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Base ARR: {a.arr} • Recommended: {a.play}</div>
            </div>
            <div className="text-right">
              <span className="text-sm font-bold text-emerald-400">{a.score} / 100</span>
              <span className="text-[10px] text-slate-500 block">{a.tier}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    print("Created diminishing returns modeler, expansion propensity, and UI studios.")

if __name__ == '__main__':
    run()
