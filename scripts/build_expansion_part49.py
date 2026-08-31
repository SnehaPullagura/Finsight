import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/marketing_channel_roas_optimizer.py
    write_file("backend/app/enterprise/crm_analytics/marketing_channel_roas_optimizer.py", """from typing import Any, Dict, List, Optional

class MarketingROASBudgetOptimizer:
    @staticmethod
    def reallocate_budget(channels: List[Dict[str, Any]], total_budget: float) -> List[Dict[str, Any]]:
        # Proportional budget weighting based on ROAS efficiency squared
        total_roas_weight = sum(float(c.get("roas", 1.0)) ** 2 for c in channels)
        
        results = []
        for c in channels:
            name = c.get("name")
            roas = float(c.get("roas", 1.0))
            weight = (roas ** 2) / max(0.01, total_roas_weight)
            allocated = round(total_budget * weight, 2)
            projected_rev = round(allocated * roas, 2)

            results.append({
                "channel_name": name,
                "historical_roas": roas,
                "recommended_budget_allocation": allocated,
                "allocation_percentage": round(weight * 100.0, 1),
                "projected_revenue": projected_rev
            })

        return sorted(results, key=lambda x: x["recommended_budget_allocation"], reverse=True)
""")

    # 2. backend/app/enterprise/customer_success/health_score_expansion_deal_builder.py
    write_file("backend/app/enterprise/customer_success/health_score_expansion_deal_builder.py", """from typing import Any, Dict, List, Optional

class ExpansionQuotePackageBuilder:
    @staticmethod
    def build_quote_proposal(account: Dict[str, Any], expansion_type: str = "SEAT_EXPANSION") -> Dict[str, Any]:
        cname = account.get("name")
        current_seats = int(account.get("current_seats", 50))
        addon_seats = int(current_seats * 0.3)
        seat_price_annual = 1200.0

        subtotal = addon_seats * seat_price_annual
        volume_discount = subtotal * 0.10
        total_amount = subtotal - volume_discount

        return {
            "proposal_title": f"{cname} — Enterprise Expansion Package",
            "expansion_type": expansion_type,
            "additional_seats_quoted": addon_seats,
            "unit_price_annual": seat_price_annual,
            "subtotal": round(subtotal, 2),
            "volume_discount_10pct": round(volume_discount, 2),
            "total_expansion_contract_value": round(total_amount, 2),
            "contract_term": "12 Months (Co-Termed to MSA)"
        }
""")

    # 3. frontend/src/enterprise/EnterpriseChannelROASOptimizerStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseChannelROASOptimizerStudio.tsx", """import React, { useState } from "react";
import { Target, TrendingUp, DollarSign, RefreshCw, CheckCircle2 } from "lucide-react";

export const EnterpriseChannelROASOptimizerStudio: React.FC = () => {
  const allocations = [
    { channel: "Google Search (High Intent)", roas: "12.4x", budget: "$45,000", pct: "45.0%", projected: "$558,000" },
    { channel: "Executive Outbound SDR", roas: "8.6x", budget: "$35,000", pct: "35.0%", projected: "$301,000" },
    { channel: "LinkedIn Account-Based Ads", roas: "5.2x", budget: "$20,000", pct: "20.0%", projected: "$104,000" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Target className="w-5 h-5 text-emerald-400" />
            Algorithmic ROAS Marketing Budget Optimizer
          </h3>
          <p className="text-xs text-slate-400">Dynamic quadratic allocation model maximizing total enterprise pipeline return on ad spend</p>
        </div>
      </div>

      <div className="space-y-3">
        {allocations.map((a, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{a.channel}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Historical ROAS: {a.roas} • Share: {a.pct}</div>
            </div>
            <div className="text-right">
              <span className="text-sm font-bold text-emerald-400">{a.budget} Budget</span>
              <span className="text-[10px] text-slate-500 block">→ {a.projected} Projected Rev</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    # 4. frontend/src/enterprise/EnterpriseExpansionDealBuilderStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseExpansionDealBuilderStudio.tsx", """import React, { useState } from "react";
import { FileText, DollarSign, CheckCircle2, Award, Plus } from "lucide-react";

export const EnterpriseExpansionDealBuilderStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <FileText className="w-5 h-5 text-emerald-400" />
            1-Click Co-Termed Expansion Quote Generator
          </h3>
          <p className="text-xs text-slate-400">Instantly generate co-termed expansion proposals with automated volume discount tiers</p>
        </div>
        <button className="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-500 text-white px-3 py-1.5 rounded-lg text-xs font-semibold shadow transition-colors">
          <Plus className="w-4 h-4" />
          Generate Quote PDF
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Additional Quoted Seats</span>
          <div className="text-2xl font-bold text-white">+15 Enterprise Seats</div>
          <span className="text-[10px] text-slate-400">$1,200 / Seat / Year</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Volume Discount Applied</span>
          <div className="text-2xl font-bold text-emerald-400">10% ($1,800 Off)</div>
          <span className="text-[10px] text-emerald-400">Pre-Approved CPQ Guardrail</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Net Contract Value</span>
          <div className="text-2xl font-bold text-emerald-400">$16,200 ARR</div>
          <span className="text-[10px] text-slate-400">Co-Termed to Master Agreement</span>
        </div>
      </div>
    </div>
  );
};
""")

    print("Created ROAS budget optimizer, quote builder, and UI studios.")

if __name__ == '__main__':
    run()
