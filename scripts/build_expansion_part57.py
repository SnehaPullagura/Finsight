import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/executive_sales_rep_ramp_payback_modeler.py
    write_file("backend/app/enterprise/crm_analytics/executive_sales_rep_ramp_payback_modeler.py", """from typing import Any, Dict, List, Optional

class RepRampPaybackModeler:
    @staticmethod
    def calculate_hiring_payback(reps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for r in reps:
            name = r.get("rep_name")
            ote_annual = float(r.get("annual_ote", 180000.0))
            monthly_base = ote_annual / 12.0
            cumulative_closed_margin = float(r.get("cumulative_closed_gross_margin", 0.0))
            tenure_months = int(r.get("tenure_months", 6))

            fully_loaded_cost = (monthly_base * tenure_months) * 1.25 # 25% overhead
            net_contribution = cumulative_closed_margin - fully_loaded_cost
            roi_multiple = round(cumulative_closed_margin / max(1.0, fully_loaded_cost), 2)

            results.append({
                "rep_name": name,
                "tenure_months": tenure_months,
                "fully_loaded_hiring_cost": round(fully_loaded_cost, 2),
                "cumulative_gross_margin_generated": cumulative_closed_margin,
                "net_profit_contribution": round(net_contribution, 2),
                "hiring_roi_multiple": roi_multiple,
                "is_payback_achieved": net_contribution > 0
            })

        return sorted(results, key=lambda x: x["hiring_roi_multiple"], reverse=True)
""")

    # 2. backend/app/enterprise/customer_success/health_score_expansion_multi_year_contract_generator.py
    write_file("backend/app/enterprise/customer_success/health_score_expansion_multi_year_contract_generator.py", """from typing import Any, Dict, List, Optional

class MultiYearContractPayloadGenerator:
    @staticmethod
    def generate_contract_agreement(account: Dict[str, Any], term_years: int, annual_rate: float) -> Dict[str, Any]:
        cname = account.get("name")
        total_tcv = annual_rate * term_years

        return {
            "agreement_title": f"Master Services Agreement Multi-Year Extension — {cname}",
            "account_name": cname,
            "term_commitment_years": term_years,
            "committed_annual_run_rate": round(annual_rate, 2),
            "total_contract_value_tcv": round(total_tcv, 2),
            "payment_terms": "Net 30 Annual Invoicing",
            "sla_tier": "Mission Critical 99.99% Availability",
            "legal_status": "DRAFT_READY_FOR_ESIGNATURE"
        }
""")

    # 3. frontend/src/enterprise/EnterpriseRepHiringPaybackStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseRepHiringPaybackStudio.tsx", """import React, { useState } from "react";
import { DollarSign, Award, TrendingUp, CheckCircle2 } from "lucide-react";

export const EnterpriseRepHiringPaybackStudio: React.FC = () => {
  const reps = [
    { name: "Alex Vance", tenure: "9 Mo", cost: "$168,750", margin: "$480,000", roi: "2.84x", status: "Payback Achieved" },
    { name: "Sarah Connor", tenure: "8 Mo", cost: "$150,000", margin: "$420,000", roi: "2.80x", status: "Payback Achieved" },
    { name: "John Wick", tenure: "6 Mo", cost: "$112,500", margin: "$85,000", roi: "0.75x", status: "In Payback Runway" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <DollarSign className="w-5 h-5 text-emerald-400" />
            Sales Rep Hiring Payback & Gross Margin Contribution
          </h3>
          <p className="text-xs text-slate-400">Fully loaded rep cost vs cumulative closed gross margin generated</p>
        </div>
      </div>

      <div className="space-y-3">
        {reps.map((r, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{r.name} ({r.tenure})</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Fully Loaded Cost: {r.cost} → Margin: {r.margin}</div>
            </div>
            <div className="text-right">
              <span className="text-sm font-bold text-emerald-400">{r.roi} ROI</span>
              <span className="text-[10px] text-slate-500 block">{r.status}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    # 4. frontend/src/enterprise/EnterpriseMultiYearContractStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseMultiYearContractStudio.tsx", """import React, { useState } from "react";
import { FileText, ShieldCheck, CheckCircle2, DollarSign } from "lucide-react";

export const EnterpriseMultiYearContractStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <FileText className="w-5 h-5 text-emerald-400" />
            Multi-Year Enterprise Agreement Generator
          </h3>
          <p className="text-xs text-slate-400">Automated legal contract drafting with co-termed commitments and SLA schedules</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Draft Ready
        </span>
      </div>

      <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold text-white">Target Account: Wayne Enterprises (3-Year Master Services Agreement)</span>
          <span className="text-xs text-emerald-400 font-semibold">$247,500 TCV</span>
        </div>
        <div className="space-y-2 text-xs text-slate-300">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>36-Month non-cancellable enterprise license commitment</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>Mission critical 99.99% availability SLA guarantee included</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>17.5% volume rate lock applied for full term duration</span>
          </div>
        </div>
      </div>
    </div>
  );
};
""")

    print("Created rep hiring payback, contract payload generator, and UI studios.")

if __name__ == '__main__':
    run()
