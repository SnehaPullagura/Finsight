import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/marketing_cac_blended_vs_paid_modeler.py
    write_file("backend/app/enterprise/crm_analytics/marketing_cac_blended_vs_paid_modeler.py", """from typing import Any, Dict, List, Optional

class CACBlendedVsPaidModeler:
    @staticmethod
    def calculate_cac_ratios(
        paid_marketing_spend: float,
        salaries_and_overhead: float,
        paid_customers_acquired: int,
        organic_customers_acquired: int
    ) -> Dict[str, Any]:
        total_customers = paid_customers_acquired + organic_customers_acquired
        total_acquisition_cost = paid_marketing_spend + salaries_and_overhead

        paid_cac = round(paid_marketing_spend / max(1, paid_customers_acquired), 2)
        blended_cac = round(total_acquisition_cost / max(1, total_customers), 2)
        organic_acquisition_pct = round((organic_customers_acquired / max(1, total_customers)) * 100.0, 1)

        return {
            "paid_marketing_spend": paid_marketing_spend,
            "fully_loaded_acquisition_cost": total_acquisition_cost,
            "paid_customers_acquired": paid_customers_acquired,
            "organic_customers_acquired": organic_customers_acquired,
            "total_customers_acquired": total_customers,
            "paid_customer_acquisition_cost": paid_cac,
            "blended_customer_acquisition_cost": blended_cac,
            "organic_acquisition_percentage": organic_acquisition_pct,
            "organic_leverage_rating": "High Organic Engine (> 40%)" if organic_acquisition_pct >= 40.0 else "Paid-Dependent (< 20%)" if organic_acquisition_pct <= 20.0 else "Balanced Acquisition"
        }
""")

    # 2. backend/app/enterprise/crm_analytics/sales_rep_win_rate_distribution.py
    write_file("backend/app/enterprise/crm_analytics/sales_rep_win_rate_distribution.py", """from typing import Any, Dict, List, Optional
from collections import defaultdict

class RepWinRateDistributionModeler:
    @staticmethod
    def analyze_team_win_rate_distribution(reps_performance: List[Dict[str, Any]]) -> Dict[str, Any]:
        win_rates = []
        tier_distribution = {"top_performers_35_plus": 0, "mid_tier_20_to_35": 0, "underperforming_sub_20": 0}

        for r in reps_performance:
            won = int(r.get("won_deals", 0))
            lost = int(r.get("lost_deals", 0))
            total = won + lost
            rate = round((won / max(1, total)) * 100.0, 1)
            win_rates.append(rate)

            if rate >= 35.0:
                tier_distribution["top_performers_35_plus"] += 1
            elif rate >= 20.0:
                tier_distribution["mid_tier_20_to_35"] += 1
            else:
                tier_distribution["underperforming_sub_20"] += 1

        team_avg_win_rate = round(sum(win_rates) / float(max(1, len(win_rates))), 1)

        return {
            "total_reps_evaluated": len(reps_performance),
            "team_average_win_rate_pct": team_avg_win_rate,
            "distribution_breakdown": tier_distribution,
            "highest_rep_win_rate": max(win_rates) if win_rates else 0.0,
            "lowest_rep_win_rate": min(win_rates) if win_rates else 0.0
        }
""")

    # 3. backend/app/enterprise/customer_success/churn_risk_early_warning_system.py
    write_file("backend/app/enterprise/customer_success/churn_risk_early_warning_system.py", """from datetime import date
from typing import Any, Dict, List, Optional

class ChurnRiskEarlyWarningSystem:
    @staticmethod
    def evaluate_account_risk_signals(account: Dict[str, Any]) -> Dict[str, Any]:
        risk_score = 0
        signals = []

        dau_drop = float(account.get("dau_drop_pct_30d", 0.0))
        if dau_drop >= 30.0:
            risk_score += 40
            signals.append(f"Product active usage dropped {dau_drop}% in last 30 days")

        nps = int(account.get("latest_nps_score", 8))
        if nps <= 6:
            risk_score += 30
            signals.append(f"Detractor NPS survey response ({nps}/10)")

        overdue_days = int(account.get("invoice_days_overdue", 0))
        if overdue_days > 14:
            risk_score += 25
            signals.append(f"Billing invoice overdue by {overdue_days} days")

        tier = "Critical Churn Risk" if risk_score >= 60 else "Elevated Risk" if risk_score >= 30 else "Healthy"

        return {
            "account_id": account.get("id"),
            "account_name": account.get("name"),
            "churn_risk_score": min(100, risk_score),
            "risk_tier": tier,
            "risk_signals": signals,
            "is_intervention_required": risk_score >= 30
        }
""")

    # 4. frontend/src/enterprise/EnterpriseRepWinRateDistributionChart.tsx
    write_file("frontend/src/enterprise/EnterpriseRepWinRateDistributionChart.tsx", """import React, { useState } from "react";
import { Award, Users, TrendingUp, CheckCircle2 } from "lucide-react";

export const EnterpriseRepWinRateDistributionChart: React.FC = () => {
  const distribution = [
    { tier: "Top Performers (35%+ Win Rate)", count: 4, pct: "33.3%", color: "text-emerald-400", bg: "bg-emerald-950/30 border-emerald-800" },
    { tier: "Core Performers (20% - 35%)", count: 6, pct: "50.0%", color: "text-blue-400", bg: "bg-blue-950/30 border-blue-800" },
    { tier: "Needs Coaching (< 20%)", count: 2, pct: "16.7%", color: "text-amber-400", bg: "bg-amber-950/30 border-amber-800" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Award className="w-5 h-5 text-emerald-400" />
            Sales Rep Win Rate Cohort Distribution
          </h3>
          <p className="text-xs text-slate-400">Team performance bell-curve and opportunity conversion consistency</p>
        </div>
        <span className="text-xs text-emerald-400 font-bold bg-emerald-950 border border-emerald-800 px-3 py-1 rounded-full">
          28.4% Team Average
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {distribution.map((d, idx) => (
          <div key={idx} className={`p-4 rounded-xl border ${d.bg} space-y-1`}>
            <span className="text-[11px] text-slate-400 font-semibold">{d.tier}</span>
            <div className={`text-2xl font-bold ${d.color}`}>{d.count} Reps</div>
            <span className="text-[10px] text-slate-500">{d.pct} of Sales Organization</span>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    # 5. frontend/src/enterprise/EnterpriseChurnEarlyWarningRadar.tsx
    write_file("frontend/src/enterprise/EnterpriseChurnEarlyWarningRadar.tsx", """import React, { useState } from "react";
import { AlertTriangle, Clock, ShieldAlert, CheckCircle2 } from "lucide-react";

export const EnterpriseChurnEarlyWarningRadar: React.FC = () => {
  const atRisk = [
    { name: "Umbrella Health Systems", arr: "$120,000", drop: "-42% DAU", nps: "5/10 (Detractor)", risk: "Critical" },
    { name: "Initech Enterprise", arr: "$85,000", drop: "-28% DAU", nps: "6/10 (Detractor)", risk: "Elevated" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-red-400" />
            Proactive Account Churn Early Warning Radar
          </h3>
          <p className="text-xs text-slate-400">Multi-signal telemetry analyzing telemetry drops and detractor NPS scores</p>
        </div>
      </div>

      <div className="space-y-3">
        {atRisk.map((a, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{a.name}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">
                ARR: {a.arr} • Signal: {a.drop} • Survey: {a.nps}
              </div>
            </div>
            <span className={`text-xs font-bold px-2.5 py-1 rounded-full ${
              a.risk === "Critical" ? "bg-red-950 text-red-400 border border-red-800" : "bg-amber-950 text-amber-400 border border-amber-800"
            }`}>
              {a.risk}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    print("Created blended CAC modeler, win rate distribution, churn warning, and UI studios.")

if __name__ == '__main__':
    run()
