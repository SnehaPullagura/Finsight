import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/marketing_creative_fatigue_index_calculator.py
    write_file("backend/app/enterprise/crm_analytics/marketing_creative_fatigue_index_calculator.py", """from typing import Any, Dict, List, Optional

class CreativeFatigueIndexCalculator:
    @staticmethod
    def calculate_fatigue_index(
        frequency: float,
        ctr_decline_pct: float,
        cpm_increase_pct: float
    ) -> Dict[str, Any]:
        # Composite fatigue index: 0 - 100
        fatigue_score = min(100.0, (frequency * 10.0) + (ctr_decline_pct * 0.4) + (cpm_increase_pct * 0.3))
        rating = "Severe Audience Fatigue (> 70)" if fatigue_score >= 70 else "Moderate Fatigue (40 - 70)" if fatigue_score >= 40 else "Fresh Creative (< 40)"

        return {
            "audience_frequency": frequency,
            "ctr_decline_pct": ctr_decline_pct,
            "cpm_increase_pct": cpm_increase_pct,
            "creative_fatigue_score": round(fatigue_score, 1),
            "fatigue_tier": rating,
            "is_creative_burnout_imminent": fatigue_score >= 60.0
        }
""")

    # 2. backend/app/enterprise/customer_success/health_score_expansion_deal_evaluator.py
    write_file("backend/app/enterprise/customer_success/health_score_expansion_deal_evaluator.py", """from typing import Any, Dict, List, Optional

class ExpansionDealHealthEvaluator:
    @staticmethod
    def evaluate_expansion_proposal_health(
        account: Dict[str, Any],
        proposed_discount_pct: float,
        term_months: int
    ) -> Dict[str, Any]:
        health = int(account.get("health_score", 50))
        nps = int(account.get("nps", 8))

        # Margin preservation score
        margin_score = max(0, 100 - int(proposed_discount_pct * 2.5))
        long_term_score = 100 if term_months >= 24 else 85 if term_months >= 12 else 50

        composite_viability = (health * 0.4) + (margin_score * 0.4) + (long_term_score * 0.2)
        score = min(100, int(composite_viability))

        return {
            "account_name": account.get("name"),
            "health_score": health,
            "proposed_discount_pct": proposed_discount_pct,
            "contract_term_months": term_months,
            "expansion_viability_score": score,
            "approval_recommendation": "AUTO_APPROVE" if score >= 80 and proposed_discount_pct <= 15.0 else "MANAGEMENT_SIGN_OFF_REQUIRED"
        }
""")

    # 3. frontend/src/enterprise/EnterpriseCreativeFatigueIndexStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseCreativeFatigueIndexStudio.tsx", """import React, { useState } from "react";
import { Flame, Target, TrendingDown, CheckCircle2 } from "lucide-react";

export const EnterpriseCreativeFatigueIndexStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Flame className="w-5 h-5 text-amber-400" />
            Ad Creative Fatigue Index & Burnout Diagnostics
          </h3>
          <p className="text-xs text-slate-400">Algorithmic fatigue score tracking audience frequency saturation and CPM inflation</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Score: 32.4 / 100 (Fresh)
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Average Frequency</span>
          <div className="text-2xl font-bold text-white">2.4x / User</div>
          <span className="text-[10px] text-emerald-400">Safe Frequency Band</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">CTR Degradation</span>
          <div className="text-2xl font-bold text-emerald-400">-4.2% MoM</div>
          <span className="text-[10px] text-slate-400">Normal Audience Variance</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">CPM Inflation</span>
          <div className="text-2xl font-bold text-white">+$1.20 CPM</div>
          <span className="text-[10px] text-emerald-400">Stable Bidding Dynamics</span>
        </div>
      </div>
    </div>
  );
};
""")

    # 4. frontend/src/enterprise/EnterpriseExpansionDealEvaluatorStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseExpansionDealEvaluatorStudio.tsx", """import React, { useState } from "react";
import { CheckCircle2, ShieldCheck, DollarSign, Award } from "lucide-react";

export const EnterpriseExpansionDealEvaluatorStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            Automated Expansion Deal Viability & Margin Gate
          </h3>
          <p className="text-xs text-slate-400">Instant validation of expansion discounts against customer health and multi-year contract terms</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Auto-Approved (Score 88/100)
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Customer Health Score</span>
          <div className="text-2xl font-bold text-emerald-400">92 / 100</div>
          <span className="text-[10px] text-emerald-400">Elite Champion Account</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Discount Concession</span>
          <div className="text-2xl font-bold text-white">10.0% Off List</div>
          <span className="text-[10px] text-emerald-400">Within Standard Tier Band</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Contract Commitment</span>
          <div className="text-2xl font-bold text-white">24 Months</div>
          <span className="text-[10px] text-emerald-400">Multi-Year Co-Termed MSA</span>
        </div>
      </div>
    </div>
  );
};
""")

    print("Created fatigue index calc, deal health evaluator, and UI studios.")

if __name__ == '__main__':
    run()
