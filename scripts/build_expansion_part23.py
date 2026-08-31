import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/deal_stage_duration_matrix.py
    write_file("backend/app/enterprise/crm_analytics/deal_stage_duration_matrix.py", """from typing import Any, Dict, List, Optional
from collections import defaultdict

class DealStageDurationMatrix:
    @staticmethod
    def analyze_stage_duration_trends(deals_history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        stage_durations = defaultdict(list)
        for h in deals_history:
            stg = h.get("stage_name", "Discovery")
            days = float(h.get("days_spent", 0.0))
            stage_durations[stg].append(days)

        results = []
        for stg, durations in stage_durations.items():
            avg_days = sum(durations) / float(len(durations)) if durations else 0.0
            med_days = sorted(durations)[len(durations) // 2] if durations else 0.0
            min_days = min(durations) if durations else 0.0
            max_days = max(durations) if durations else 0.0

            results.append({
                "stage": stg,
                "average_days_in_stage": round(avg_days, 1),
                "median_days": round(med_days, 1),
                "min_days": round(min_days, 1),
                "max_days": round(max_days, 1),
                "sample_deal_count": len(durations)
            })

        return results
""")

    # 2. backend/app/enterprise/crm_analytics/marketing_cac_payback_modeler.py
    write_file("backend/app/enterprise/crm_analytics/marketing_cac_payback_modeler.py", """from typing import Any, Dict, List, Optional

class CACPaybackModeler:
    @staticmethod
    def calculate_payback_months(
        customer_acquisition_cost: float,
        monthly_arpu: float,
        gross_margin_percentage: float
    ) -> Dict[str, Any]:
        margin_decimal = gross_margin_percentage / 100.0
        monthly_gross_profit = monthly_arpu * margin_decimal

        if monthly_gross_profit <= 0:
            return {"payback_months": 999.0, "status": "unprofitable"}

        payback_months = round(customer_acquisition_cost / monthly_gross_profit, 1)

        return {
            "customer_acquisition_cost": customer_acquisition_cost,
            "monthly_arpu": monthly_arpu,
            "gross_margin_percentage": gross_margin_percentage,
            "monthly_gross_profit_per_customer": round(monthly_gross_profit, 2),
            "payback_period_months": payback_months,
            "capital_efficiency_grade": "Top Decile (< 12 Mo)" if payback_months <= 12.0 else "Healthy (12-18 Mo)" if payback_months <= 18.0 else "High Burn (> 18 Mo)"
        }
""")

    # 3. backend/app/enterprise/customer_success/onboarding_milestone_tracker.py
    write_file("backend/app/enterprise/customer_success/onboarding_milestone_tracker.py", """from datetime import date
from typing import Any, Dict, List, Optional

class OnboardingMilestoneTracker:
    @staticmethod
    def evaluate_onboarding_health(milestones: List[Dict[str, Any]], elapsed_days: int) -> Dict[str, Any]:
        total = len(milestones)
        completed = sum(1 for m in milestones if m.get("is_completed"))
        completion_pct = round((completed / max(1, total)) * 100.0, 1)

        # Expected milestone completion pacing
        expected_completed = min(total, int((elapsed_days / 30.0) * total))
        is_delayed = completed < expected_completed

        return {
            "total_milestones": total,
            "completed_milestones": completed,
            "completion_percentage": completion_pct,
            "elapsed_days": elapsed_days,
            "is_onboarding_delayed": is_delayed,
            "onboarding_status": "On Schedule" if not is_delayed else "Needs CSM Escalation"
        }
""")

    # 4. frontend/src/enterprise/EnterpriseStageDurationMatrix.tsx
    write_file("frontend/src/enterprise/EnterpriseStageDurationMatrix.tsx", """import React, { useState } from "react";
import { Clock, TrendingUp, BarChart3 } from "lucide-react";

export const EnterpriseStageDurationMatrix: React.FC = () => {
  const durations = [
    { stage: "Discovery Call", avg: "4.2d", median: "3.5d", min: "1d", max: "12d" },
    { stage: "Technical Scoping", avg: "8.5d", median: "7.0d", min: "3d", max: "21d" },
    { stage: "CPQ Quote Generation", avg: "5.1d", median: "4.0d", min: "1d", max: "14d" },
    { stage: "Executive Negotiation", avg: "14.8d", median: "12.0d", min: "5d", max: "45d" },
    { stage: "Legal & Procurement", avg: "12.0d", median: "10.0d", min: "4d", max: "30d" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Clock className="w-5 h-5 text-emerald-400" />
            Stage Duration Distribution & Sales Pacing
          </h3>
          <p className="text-xs text-slate-400">Average, median, and maximum days spent by opportunities across pipeline stages</p>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-xs text-left">
          <thead className="bg-slate-950 text-slate-400 font-semibold border-b border-slate-800">
            <tr>
              <th className="p-3">Sales Pipeline Stage</th>
              <th className="p-3 text-right">Average Days</th>
              <th className="p-3 text-right">Median Days</th>
              <th className="p-3 text-right">Min Days</th>
              <th className="p-3 text-right">Max Days</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-white">
            {durations.map((d, idx) => (
              <tr key={idx} className="hover:bg-slate-800/30">
                <td className="p-3 font-semibold">{d.stage}</td>
                <td className="p-3 text-right font-bold text-emerald-400">{d.avg}</td>
                <td className="p-3 text-right text-slate-300">{d.median}</td>
                <td className="p-3 text-right text-slate-500">{d.min}</td>
                <td className="p-3 text-right text-amber-400">{d.max}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
""")

    # 5. frontend/src/enterprise/EnterpriseOnboardingMilestones.tsx
    write_file("frontend/src/enterprise/EnterpriseOnboardingMilestones.tsx", """import React, { useState } from "react";
import { CheckCircle2, Circle, Clock, ArrowRight, ShieldCheck } from "lucide-react";

export const EnterpriseOnboardingMilestones: React.FC = () => {
  const milestones = [
    { title: "Kickoff & Architecture Review", day: "Day 1", completed: true },
    { title: "SSO & Identity Provider Verification", day: "Day 7", completed: true },
    { title: "Historical Data Migration & Mapping", day: "Day 14", completed: true },
    { title: "Sales Team Workflow Certification", day: "Day 21", completed: false },
    { title: "Executive Go-Live Sign-Off", day: "Day 30", completed: false }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            Enterprise White-Glove Onboarding Milestones
          </h3>
          <p className="text-xs text-slate-400">30-day time-to-value implementation milestones for enterprise accounts</p>
        </div>
        <span className="text-xs text-emerald-400 font-bold bg-emerald-950 border border-emerald-800 px-3 py-1 rounded-full">
          60% Completed (On Schedule)
        </span>
      </div>

      <div className="space-y-3">
        {milestones.map((m, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div className="flex items-center gap-3">
              {m.completed ? (
                <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
              ) : (
                <Circle className="w-5 h-5 text-slate-600 shrink-0" />
              )}
              <div>
                <div className={`text-xs font-bold ${m.completed ? "text-white" : "text-slate-400"}`}>{m.title}</div>
                <div className="text-[10px] text-slate-500">{m.day} Target</div>
              </div>
            </div>
            <span className={`text-xs font-semibold ${m.completed ? "text-emerald-400" : "text-slate-500"}`}>
              {m.completed ? "Completed" : "In Progress"}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    print("Created stage duration matrix, payback modeler, milestone tracker, and UI modules.")

if __name__ == '__main__':
    run()
