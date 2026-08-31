import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/deal_slippage_risk_engine.py
    write_file("backend/app/enterprise/crm_analytics/deal_slippage_risk_engine.py", """from datetime import date, timedelta
from typing import Any, Dict, List, Optional

class DealSlippageRiskEngine:
    @staticmethod
    def evaluate_deal_close_date_risk(deal: Dict[str, Any], push_count: int, stage_days: int) -> Dict[str, Any]:
        close_date_str = deal.get("expected_close_date") or date.today().isoformat()
        close_date = date.fromisoformat(close_date_str)
        today = date.today()

        days_until_close = (close_date - today).days
        risk_score = 0
        risk_signals = []

        if days_until_close < 0:
            risk_score += 50
            risk_signals.append(f"Close date is {abs(days_until_close)} days in the past")
        elif days_until_close <= 5 and deal.get("stage") in ["Discovery", "Scoping"]:
            risk_score += 40
            risk_signals.append("Close date within 5 days but deal is in early stage")

        if push_count >= 3:
            risk_score += 30
            risk_signals.append(f"Close date has been pushed {push_count} times")
        elif push_count >= 1:
            risk_score += 15
            risk_signals.append(f"Close date has been pushed {push_count} time(s)")

        if stage_days > 21:
            risk_score += 20
            risk_signals.append(f"Deal stalled in current stage for {stage_days} days")

        final_risk = min(100, risk_score)
        tier = "Critical Slippage Risk" if final_risk >= 70 else "Elevated Risk" if final_risk >= 40 else "On Schedule"

        return {
            "deal_id": deal.get("id"),
            "deal_name": deal.get("name"),
            "expected_close_date": close_date.isoformat(),
            "slippage_risk_score": final_risk,
            "risk_tier": tier,
            "risk_signals": risk_signals,
            "push_count": push_count,
            "is_slippage_likely": final_risk >= 40
        }
""")

    # 2. backend/app/enterprise/crm_analytics/win_loss_decision_matrix.py
    write_file("backend/app/enterprise/crm_analytics/win_loss_decision_matrix.py", """from typing import Any, Dict, List, Optional
from collections import defaultdict

class WinLossDecisionMatrix:
    @staticmethod
    def analyze_win_loss_patterns(closed_deals: List[Dict[str, Any]]) -> Dict[str, Any]:
        won_reasons = defaultdict(int)
        lost_reasons = defaultdict(int)
        competitor_wins = defaultdict(int)

        total_won = 0
        total_lost = 0

        for d in closed_deals:
            status = (d.get("status") or "").lower()
            reason = d.get("win_loss_reason") or "Not Specified"
            comp = d.get("competitor_lost_to")

            if status == "won":
                total_won += 1
                won_reasons[reason] += 1
            elif status == "lost":
                total_lost += 1
                lost_reasons[reason] += 1
                if comp:
                    competitor_wins[comp] += 1

        overall_win_rate = round((total_won / max(1, total_won + total_lost)) * 100.0, 1)

        return {
            "total_closed_deals": total_won + total_lost,
            "total_won": total_won,
            "total_lost": total_lost,
            "win_rate_percentage": overall_win_rate,
            "top_won_reasons": sorted([{"reason": k, "count": v} for k, v in won_reasons.items()], key=lambda x: x["count"], reverse=True),
            "top_lost_reasons": sorted([{"reason": k, "count": v} for k, v in lost_reasons.items()], key=lambda x: x["count"], reverse=True),
            "competitor_losses": sorted([{"competitor": k, "losses_count": v} for k, v in competitor_wins.items()], key=lambda x: x["losses_count"], reverse=True)
        }
""")

    # 3. backend/app/enterprise/security_governance/abac_policy_compiler.py
    write_file("backend/app/enterprise/security_governance/abac_policy_compiler.py", """from typing import Any, Dict, List, Optional

class ABACPolicyCompiler:
    @staticmethod
    def compile_policy_rules(policies: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        compiled = defaultdict(list)
        for p in policies:
            resource = p.get("resource", "*")
            compiled[resource].append(p)
        return dict(compiled)

    @staticmethod
    def evaluate_access(user: Dict[str, Any], resource_name: str, action: str, compiled_policies: Dict[str, List[Dict[str, Any]]]) -> bool:
        user_roles = set(user.get("roles", []))
        if "Admin" in user_roles or user.get("is_superuser"):
            return True

        matching_policies = compiled_policies.get(resource_name, []) + compiled_policies.get("*", [])
        for p in matching_policies:
            if p.get("action") in [action, "*"]:
                allowed_roles = set(p.get("conditions", {}).get("roles", []))
                if allowed_roles and user_roles.intersection(allowed_roles):
                    return p.get("effect", "allow") == "allow"

        return False
""")

    # 4. frontend/src/enterprise/EnterpriseDealSlippageMatrix.tsx
    write_file("frontend/src/enterprise/EnterpriseDealSlippageMatrix.tsx", """import React, { useState } from "react";
import { AlertCircle, Clock, CheckCircle2, TrendingDown } from "lucide-react";

export const EnterpriseDealSlippageMatrix: React.FC = () => {
  const atRiskDeals = [
    { name: "Wayne Enterprises Global MSA", value: "$250,000", pushCount: 3, daysStagnant: 28, risk: "Critical" },
    { name: "Oscorp Enterprise AI Rollout", value: "$180,000", pushCount: 2, daysStagnant: 18, risk: "Elevated" },
    { name: "Cyberdyne Systems Security Suite", value: "$95,000", pushCount: 1, daysStagnant: 12, risk: "Moderate" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <TrendingDown className="w-5 h-5 text-amber-400" />
            Deal Slippage Early Warning System
          </h3>
          <p className="text-xs text-slate-400">Identify deals with multiple close date delays and stage stagnation</p>
        </div>
      </div>

      <div className="space-y-3">
        {atRiskDeals.map((deal, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{deal.name}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">
                {deal.value} • Pushed {deal.pushCount} times • {deal.daysStagnant} days in stage
              </div>
            </div>
            <span className={`text-xs font-bold px-2.5 py-1 rounded-full ${
              deal.risk === "Critical" ? "bg-red-950 text-red-400 border border-red-800" :
              deal.risk === "Elevated" ? "bg-amber-950 text-amber-400 border border-amber-800" : "bg-blue-950 text-blue-400 border border-blue-800"
            }`}>
              {deal.risk}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    # 5. frontend/src/enterprise/EnterpriseWinLossAnalysisStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseWinLossAnalysisStudio.tsx", """import React, { useState } from "react";
import { Award, PieChart, CheckCircle2, XCircle } from "lucide-react";

export const EnterpriseWinLossAnalysisStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <PieChart className="w-5 h-5 text-emerald-400" />
            Win / Loss Decision Matrix & Competitor Insights
          </h3>
          <p className="text-xs text-slate-400">Quantitative reasons for closed won and closed lost opportunities</p>
        </div>
        <div className="text-right">
          <span className="text-[11px] text-slate-400">Quarterly Win Rate</span>
          <div className="text-xl font-bold text-emerald-400">68.4%</div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-2">
          <span className="text-xs font-bold text-emerald-400 flex items-center gap-1.5">
            <CheckCircle2 className="w-4 h-4" /> Top Drivers for Closed Won
          </span>
          <ul className="space-y-1.5 text-xs text-slate-300">
            <li>1. Superior DAG Workflow Customization (42%)</li>
            <li>2. Out-of-the-Box Multi-Tenant Security (28%)</li>
            <li>3. Transparent Predictable CPQ Pricing (18%)</li>
          </ul>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-2">
          <span className="text-xs font-bold text-red-400 flex items-center gap-1.5">
            <XCircle className="w-4 h-4" /> Top Drivers for Closed Lost
          </span>
          <ul className="space-y-1.5 text-xs text-slate-300">
            <li>1. Budget Freeze / Economic Headwinds (50%)</li>
            <li>2. Preferred Existing Legacy Vendor (30%)</li>
            <li>3. Implementation Timeline Fit (20%)</li>
          </ul>
        </div>
      </div>
    </div>
  );
};
""")

    print("Created deal slippage engine, win-loss matrix, ABAC compiler, and UI studios.")

if __name__ == '__main__':
    run()
