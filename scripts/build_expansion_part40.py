import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/executive_tam_penetration_curve.py
    write_file("backend/app/enterprise/crm_analytics/executive_tam_penetration_curve.py", """from typing import Any, Dict, List, Optional

class TAMPenetrationCurveAnalyzer:
    @staticmethod
    def calculate_penetration_pacing(
        total_market_accounts: int,
        acquired_accounts: int,
        pipeline_engaged_accounts: int,
        annual_growth_rate_pct: float
    ) -> Dict[str, Any]:
        penetration_pct = round((acquired_accounts / max(1, total_market_accounts)) * 100.0, 2)
        engaged_pct = round((pipeline_engaged_accounts / max(1, total_market_accounts)) * 100.0, 2)
        unreached_accounts = max(0, total_market_accounts - acquired_accounts - pipeline_engaged_accounts)

        return {
            "total_market_accounts": total_market_accounts,
            "acquired_customers_count": acquired_accounts,
            "current_market_penetration_pct": penetration_pct,
            "pipeline_engaged_accounts": pipeline_engaged_accounts,
            "pipeline_engaged_pct": engaged_pct,
            "unreached_white_space_accounts": unreached_accounts,
            "market_share_tier": "Dominant Player (> 15%)" if penetration_pct >= 15.0 else "Established Challenger (5% - 15%)" if penetration_pct >= 5.0 else "Early Market Entrant (< 5%)"
        }
""")

    # 2. backend/app/enterprise/customer_success/health_score_predictive_renewal_risk.py
    write_file("backend/app/enterprise/customer_success/health_score_predictive_renewal_risk.py", """from typing import Any, Dict, List, Optional

class PredictiveRenewalRiskModeler:
    @staticmethod
    def predict_contract_renewal(account: Dict[str, Any], days_until_renewal: int) -> Dict[str, Any]:
        health_score = int(account.get("health_score", 50))
        nps = int(account.get("nps", 8))
        sponsor_active = bool(account.get("is_executive_sponsor_engaged", True))

        # Base renewal probability from health score
        base_prob = health_score * 0.7 + (nps * 3.0)
        if not sponsor_active:
            base_prob -= 25.0

        renewal_probability = min(100.0, max(5.0, round(base_prob, 1)))

        risk_category = "High Renewal Risk" if renewal_probability < 50.0 else "Moderate Risk" if renewal_probability < 75.0 else "Safe On-Track Renewal"

        return {
            "account_id": account.get("id"),
            "account_name": account.get("name"),
            "contract_arr": account.get("current_arr"),
            "days_until_renewal": days_until_renewal,
            "health_score": health_score,
            "renewal_probability_percentage": renewal_probability,
            "risk_category": risk_category,
            "action_required": "SCHEDULE_EXECUTIVE_ALIGNMENT" if renewal_probability < 75.0 else "STANDARD_RENEWAL_CADENCE"
        }
""")

    # 3. frontend/src/enterprise/EnterpriseTAMPenetrationCurveStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseTAMPenetrationCurveStudio.tsx", """import React, { useState } from "react";
import { Globe, TrendingUp, PieChart, CheckCircle2 } from "lucide-react";

export const EnterpriseTAMPenetrationCurveStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Globe className="w-5 h-5 text-emerald-400" />
            Market TAM Penetration & White-Space Radar
          </h3>
          <p className="text-xs text-slate-400">Total addressable market account penetration vs actively engaged pipeline accounts</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          7.2% Penetration (Challenger)
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Acquired Customer Accounts</span>
          <div className="text-2xl font-bold text-emerald-400">864 Accounts</div>
          <span className="text-[10px] text-slate-400">7.2% of Total 12,000 Target TAM</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Active Pipeline Engaged</span>
          <div className="text-2xl font-bold text-white">1,420 Accounts</div>
          <span className="text-[10px] text-emerald-400">11.8% of Total TAM in Motion</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Unreached White Space</span>
          <div className="text-2xl font-bold text-slate-400">9,716 Accounts</div>
          <span className="text-[10px] text-slate-400">81.0% Expansion Opportunity</span>
        </div>
      </div>
    </div>
  );
};
""")

    # 4. frontend/src/enterprise/EnterprisePredictiveRenewalStudio.tsx
    write_file("frontend/src/enterprise/EnterprisePredictiveRenewalStudio.tsx", """import React, { useState } from "react";
import { Calendar, ShieldAlert, CheckCircle2, TrendingUp, AlertTriangle } from "lucide-react";

export const EnterprisePredictiveRenewalStudio: React.FC = () => {
  const renewals = [
    { name: "Acme Global Industries", arr: "$320,000", days: 45, prob: "94%", status: "Safe On-Track" },
    { name: "Stark Tech Enterprises", arr: "$250,000", days: 60, prob: "88%", status: "Safe On-Track" },
    { name: "Cyberdyne Systems", arr: "$140,000", days: 30, prob: "52%", status: "Moderate Risk" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Calendar className="w-5 h-5 text-emerald-400" />
            Predictive Contract Renewal & Retention Modeler
          </h3>
          <p className="text-xs text-slate-400">Algorithmic renewal probabilities based on product usage, NPS, and executive sponsor engagement</p>
        </div>
      </div>

      <div className="space-y-3">
        {renewals.map((r, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{r.name}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">
                ARR: {r.arr} • Renewing in {r.days} days • Probability: <span className="text-emerald-400 font-bold">{r.prob}</span>
              </div>
            </div>
            <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${
              r.status === "Safe On-Track" ? "bg-emerald-950 text-emerald-400 border border-emerald-800" : "bg-amber-950 text-amber-400 border border-amber-800"
            }`}>
              {r.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    print("Created TAM penetration curve, renewal risk modeler, and UI studios.")

if __name__ == '__main__':
    run()
