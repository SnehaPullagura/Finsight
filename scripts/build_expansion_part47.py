import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/marketing_cac_payback_sensitivity.py
    write_file("backend/app/enterprise/crm_analytics/marketing_cac_payback_sensitivity.py", """from typing import Any, Dict, List, Optional

class CACPaybackSensitivityModeler:
    @staticmethod
    def simulate_churn_sensitivity(
        base_cac: float,
        monthly_arpu: float,
        gross_margin_pct: float,
        churn_rates: List[float] = [0.5, 1.0, 1.5, 2.0, 2.5]
    ) -> List[Dict[str, Any]]:
        results = []
        gp = monthly_arpu * (gross_margin_pct / 100.0)

        for cr in churn_rates:
            payback = round(base_cac / max(1.0, gp), 1)
            ltv = round(gp / max(0.001, cr / 100.0), 2)
            ltv_cac = round(ltv / max(1.0, base_cac), 2)

            results.append({
                "monthly_churn_pct": cr,
                "gross_profit_per_customer": round(gp, 2),
                "payback_months": payback,
                "implied_ltv": ltv,
                "ltv_to_cac_ratio": ltv_cac,
                "economics_health": "Exceptional (> 5.0x)" if ltv_cac >= 5.0 else "Healthy (3.0x - 5.0x)" if ltv_cac >= 3.0 else "Vulnerable (< 3.0x)"
            })

        return results
""")

    # 2. backend/app/enterprise/customer_success/health_score_expansion_attribution_matrix.py
    write_file("backend/app/enterprise/customer_success/health_score_expansion_attribution_matrix.py", """from typing import Any, Dict, List, Optional

class CSExpansionAttributionMatrix:
    @staticmethod
    def attribute_expansion_revenue(deals: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_expansion = 0.0
        cs_assisted = 0.0
        product_led = 0.0
        sales_outbound = 0.0

        for d in deals:
            val = float(d.get("deal_value", 0.0))
            src = d.get("lead_source", "")
            total_expansion += val

            if "CS Health" in src or "Customer Success" in src:
                cs_assisted += val
            elif "Product" in src or "Self-Service" in src:
                product_led += val
            else:
                sales_outbound += val

        cs_pct = round((cs_assisted / max(1.0, total_expansion)) * 100.0, 1)

        return {
            "total_expansion_revenue": round(total_expansion, 2),
            "cs_health_assisted_revenue": round(cs_assisted, 2),
            "product_led_expansion_revenue": round(product_led, 2),
            "sales_outbound_expansion_revenue": round(sales_outbound, 2),
            "cs_assisted_percentage": cs_pct
        }
""")

    # 3. frontend/src/enterprise/EnterpriseCACPaybackSensitivityStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseCACPaybackSensitivityStudio.tsx", """import React, { useState } from "react";
import { Calculator, TrendingUp, DollarSign, CheckCircle2 } from "lucide-react";

export const EnterpriseCACPaybackSensitivityStudio: React.FC = () => {
  const sensitivities = [
    { churn: "0.5% / Mo", payback: "7.2 Mo", ltv: "$240,000", ratio: "8.2x", health: "Exceptional" },
    { churn: "1.0% / Mo", payback: "7.2 Mo", ltv: "$120,000", ratio: "4.1x", health: "Healthy" },
    { churn: "2.0% / Mo", payback: "7.2 Mo", ltv: "$60,000", ratio: "2.1x", health: "Vulnerable" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Calculator className="w-5 h-5 text-emerald-400" />
            CAC Payback & Churn Sensitivity Matrix
          </h3>
          <p className="text-xs text-slate-400">Stress-testing unit economics and LTV:CAC multiples under fluctuating churn rate scenarios</p>
        </div>
      </div>

      <div className="space-y-3">
        {sensitivities.map((s, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">Scenario: {s.churn} Churn</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Payback: {s.payback} • Implied LTV: {s.ltv}</div>
            </div>
            <div className="text-right">
              <span className="text-sm font-bold text-emerald-400">{s.ratio} LTV:CAC</span>
              <span className="text-[10px] text-slate-500 block">{s.health}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    # 4. frontend/src/enterprise/EnterpriseExpansionAttributionStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseExpansionAttributionStudio.tsx", """import React, { useState } from "react";
import { TrendingUp, Layers, CheckCircle2, Award } from "lucide-react";

export const EnterpriseExpansionAttributionStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Layers className="w-5 h-5 text-emerald-400" />
            Expansion Revenue Attribution & Sourcing Matrix
          </h3>
          <p className="text-xs text-slate-400">Deconstruct expansion ARR sourced by Customer Success signals vs Product-Led growth</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          +$2.85M Expansion ARR
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">CS Health Assisted</span>
          <div className="text-2xl font-bold text-emerald-400">$1,650,000</div>
          <span className="text-[10px] text-slate-400">57.9% of Total Expansion</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Product-Led Add-Ons</span>
          <div className="text-2xl font-bold text-white">$820,000</div>
          <span className="text-[10px] text-emerald-400">28.8% Self-Service Upsell</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Sales Outbound Upsell</span>
          <div className="text-2xl font-bold text-white">$380,000</div>
          <span className="text-[10px] text-slate-400">13.3% Strategic Renewals</span>
        </div>
      </div>
    </div>
  );
};
""")

    print("Created payback sensitivity, expansion attribution, and UI studios.")

if __name__ == '__main__':
    run()
