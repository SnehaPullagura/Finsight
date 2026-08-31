import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/executive_sales_rep_ramp_milestone_tracker.py
    write_file("backend/app/enterprise/crm_analytics/executive_sales_rep_ramp_milestone_tracker.py", """from datetime import date
from typing import Any, Dict, List, Optional

class RepRampMilestoneTracker:
    @staticmethod
    def audit_onboarding_milestones(reps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for r in reps:
            name = r.get("rep_name")
            tenure_months = int(r.get("tenure_months", 1))
            first_deal_closed = bool(r.get("first_deal_closed", False))
            pipeline_built = float(r.get("pipeline_dollars_built", 0.0))

            if tenure_months <= 3:
                expected_pipeline = 100000.0
            elif tenure_months <= 6:
                expected_pipeline = 300000.0
            else:
                expected_pipeline = 600000.0

            pacing_pct = round((pipeline_built / max(1.0, expected_pipeline)) * 100.0, 1)

            results.append({
                "rep_name": name,
                "tenure_months": tenure_months,
                "first_deal_closed": first_deal_closed,
                "pipeline_built": pipeline_built,
                "expected_pipeline_benchmark": expected_pipeline,
                "ramp_pacing_percentage": pacing_pct,
                "ramp_status": "Ahead of Schedule" if pacing_pct >= 120.0 else "On Track" if pacing_pct >= 90.0 else "Needs Ramp Coaching"
            })

        return sorted(results, key=lambda x: x["ramp_pacing_percentage"], reverse=True)
""")

    # 2. backend/app/enterprise/customer_success/health_score_expansion_multi_year_discount_matrix.py
    write_file("backend/app/enterprise/customer_success/health_score_expansion_multi_year_discount_matrix.py", """from typing import Any, Dict, List, Optional

class MultiYearDiscountMatrix:
    @staticmethod
    def calculate_multi_year_terms(annual_contract_value: float) -> List[Dict[str, Any]]:
        tiers = [
            {"term_years": 1, "discount_pct": 0.0, "upfront_payment_pct": 100.0},
            {"term_years": 2, "discount_pct": 10.0, "upfront_payment_pct": 100.0},
            {"term_years": 3, "discount_pct": 17.5, "upfront_payment_pct": 100.0},
            {"term_years": 5, "discount_pct": 25.0, "upfront_payment_pct": 100.0}
        ]

        results = []
        for t in tiers:
            discount = t["discount_pct"]
            years = t["term_years"]
            discounted_annual = annual_contract_value * (1.0 - (discount / 100.0))
            total_tcv = discounted_annual * years

            results.append({
                "commitment_term_years": years,
                "discount_percentage": discount,
                "annualized_rate": round(discounted_annual, 2),
                "total_contract_value": round(total_tcv, 2),
                "total_customer_savings": round((annual_contract_value * years) - total_tcv, 2)
            })

        return results
""")

    # 3. frontend/src/enterprise/EnterpriseRepRampMilestoneStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseRepRampMilestoneStudio.tsx", """import React, { useState } from "react";
import { UserCheck, Award, TrendingUp, CheckCircle2 } from "lucide-react";

export const EnterpriseRepRampMilestoneStudio: React.FC = () => {
  const reps = [
    { name: "Jessica Alba", tenure: "2 Months", built: "$145,000", target: "$100,000", pacing: "145.0%", status: "Ahead of Schedule" },
    { name: "Marcus Wright", tenure: "4 Months", built: "$280,000", target: "$300,000", pacing: "93.3%", status: "On Track" },
    { name: "Kyle Reese", tenure: "5 Months", built: "$180,000", target: "$300,000", pacing: "60.0%", status: "Needs Ramp Coaching" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <UserCheck className="w-5 h-5 text-emerald-400" />
            New Sales Hire Ramp Velocity & Milestone Pacing
          </h3>
          <p className="text-xs text-slate-400">Tracks pipeline generation benchmarks and deal closing pacing during initial 6-month ramp</p>
        </div>
      </div>

      <div className="space-y-3">
        {reps.map((r, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{r.name} ({r.tenure})</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Pipeline Built: {r.built} / {r.target} Benchmark</div>
            </div>
            <div className="text-right">
              <span className="text-sm font-bold text-emerald-400">{r.pacing} Pacing</span>
              <span className="text-[10px] text-slate-500 block">{r.status}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    # 4. frontend/src/enterprise/EnterpriseMultiYearDiscountStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseMultiYearDiscountStudio.tsx", """import React, { useState } from "react";
import { DollarSign, ShieldCheck, CheckCircle2, Award } from "lucide-react";

export const EnterpriseMultiYearDiscountStudio: React.FC = () => {
  const tiers = [
    { term: "1 Year Standard", disc: "0.0%", annual: "$100,000", tcv: "$100,000", savings: "$0" },
    { term: "2 Year Strategic", disc: "10.0%", annual: "$90,000", tcv: "$180,000", savings: "$20,000" },
    { term: "3 Year Enterprise", disc: "17.5%", annual: "$82,500", tcv: "$247,500", savings: "$52,500" },
    { term: "5 Year Transformational", disc: "25.0%", annual: "$75,000", tcv: "$375,000", savings: "$125,000" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <DollarSign className="w-5 h-5 text-emerald-400" />
            Multi-Year Commitment Discount & TCV Optimizer
          </h3>
          <p className="text-xs text-slate-400">Standardized multi-year discount schedules maximizing Total Contract Value (TCV) retention</p>
        </div>
      </div>

      <div className="space-y-3">
        {tiers.map((t, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{t.term}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Discount: {t.disc} • Annualized: {t.annual} • Total Savings: <span className="text-emerald-400 font-bold">{t.savings}</span></div>
            </div>
            <div className="text-right">
              <span className="text-sm font-bold text-emerald-400">{t.tcv} TCV</span>
              <span className="text-[10px] text-slate-500 block">Pre-Approved CPQ Guard</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    print("Created rep ramp milestones, multi-year discount matrix, and UI studios.")

if __name__ == '__main__':
    run()
