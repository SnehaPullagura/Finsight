import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/executive_sales_rep_ramp_payback_schedule.py
    write_file("backend/app/enterprise/crm_analytics/executive_sales_rep_ramp_payback_schedule.py", """from typing import Any, Dict, List, Optional

class RepHiringPaybackSchedule:
    @staticmethod
    def generate_monthly_payback_curve(monthly_cost: float, monthly_margin_ramp: List[float]) -> List[Dict[str, Any]]:
        curve = []
        cumulative_cost = 0.0
        cumulative_margin = 0.0

        for m, margin in enumerate(monthly_margin_ramp, start=1):
            cumulative_cost += monthly_cost
            cumulative_margin += margin
            net = cumulative_margin - cumulative_cost

            curve.append({
                "month": m,
                "cumulative_cost": round(cumulative_cost, 2),
                "cumulative_margin": round(cumulative_margin, 2),
                "net_profit_loss": round(net, 2),
                "is_profitable": net >= 0
            })

        return curve
""")

    # 2. backend/app/enterprise/customer_success/health_score_expansion_multi_year_sla_generator.py
    write_file("backend/app/enterprise/customer_success/health_score_expansion_multi_year_sla_generator.py", """from typing import Any, Dict, List, Optional

class MultiYearSLAPackageGenerator:
    @staticmethod
    def generate_sla_package(sla_tier: str = "MISSION_CRITICAL") -> Dict[str, Any]:
        return {
            "sla_tier": sla_tier,
            "uptime_commitment_pct": 99.99,
            "sev1_response_time_minutes": 15,
            "sev2_response_time_hours": 2,
            "dedicated_named_tam_assigned": True,
            "financial_service_credits": {
                "below_99_9pct": "10% Monthly Credit",
                "below_99_5pct": "25% Monthly Credit",
                "below_99_0pct": "50% Monthly Credit"
            },
            "sla_status": "BINDING_CONTRACT_ATTACHED"
        }
""")

    # 3. frontend/src/enterprise/EnterpriseRepPaybackScheduleStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseRepPaybackScheduleStudio.tsx", """import React, { useState } from "react";
import { TrendingUp, DollarSign, CheckCircle2, Award } from "lucide-react";

export const EnterpriseRepPaybackScheduleStudio: React.FC = () => {
  const curve = [
    { month: "Month 1", cost: "$18,750", margin: "$0", net: "-$18,750", status: "Ramping" },
    { month: "Month 3", cost: "$56,250", margin: "$25,000", net: "-$31,250", status: "Ramping" },
    { month: "Month 6", cost: "$112,500", margin: "$120,000", net: "+$7,500", status: "Payback Hit" },
    { month: "Month 9", cost: "$168,750", margin: "$280,000", net: "+$111,250", status: "Highly Profitable" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-emerald-400" />
            Monthly Sales Rep Hiring Payback Schedule
          </h3>
          <p className="text-xs text-slate-400">Cumulative fully-loaded compensation against gross profit margin contribution curve</p>
        </div>
      </div>

      <div className="space-y-3">
        {curve.map((c, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{c.month}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Cumulative Cost: {c.cost} • Margin: {c.margin}</div>
            </div>
            <div className="text-right">
              <span className={`text-sm font-bold ${c.net.startsWith("+") ? "text-emerald-400" : "text-amber-400"}`}>{c.net}</span>
              <span className="text-[10px] text-slate-500 block">{c.status}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    # 4. frontend/src/enterprise/EnterpriseMultiYearSLAStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseMultiYearSLAStudio.tsx", """import React, { useState } from "react";
import { ShieldCheck, Award, CheckCircle2, Clock } from "lucide-react";

export const EnterpriseMultiYearSLAStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            Mission-Critical Enterprise SLA & Service Credit Schedule
          </h3>
          <p className="text-xs text-slate-400">Multi-year contractual uptime guarantees with automated financial credit schedules</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          99.99% Guaranteed
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Sev-1 Response Time</span>
          <div className="text-2xl font-bold text-emerald-400">&lt; 15 Mins</div>
          <span className="text-[10px] text-slate-400">24x7x365 Hotline</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Dedicated TAM</span>
          <div className="text-2xl font-bold text-white">Assigned</div>
          <span className="text-[10px] text-emerald-400">Named Technical Architect</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Max Credit Offset</span>
          <div className="text-2xl font-bold text-white">50% Credit</div>
          <span className="text-[10px] text-slate-400">If Uptime Drops Below 99.0%</span>
        </div>
      </div>
    </div>
  );
};
""")

    print("Created payback schedule, multi-year SLA, and UI studios.")

if __name__ == '__main__':
    run()
