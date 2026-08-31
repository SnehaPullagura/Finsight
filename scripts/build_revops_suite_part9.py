import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/sales_compensation/commission_clawback_engine.py
    write_file("backend/app/enterprise/sales_compensation/commission_clawback_engine.py", """from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class CommissionClawbackEngine:
    \"\"\"
    Audits early contract cancellations and computes commission clawbacks:
    - 0-90 Days: 100% Commission Clawback
    - 91-180 Days: 50% Commission Clawback
    - 181+ Days: 0% Clawback (Standard Retention Risk)
    \"\"\"
    @staticmethod
    def evaluate_deal_churn_clawback(
        deal_id: str,
        rep_name: str,
        commission_paid: float,
        days_active_before_cancel: int
    ) -> Dict[str, Any]:
        if days_active_before_cancel <= 90:
            clawback_pct = 100.0
        elif days_active_before_cancel <= 180:
            clawback_pct = 50.0
        else:
            clawback_pct = 0.0

        clawback_amount = round(commission_paid * (clawback_pct / 100.0), 2)
        net_retained = round(commission_paid - clawback_amount, 2)

        return {
            "deal_id": deal_id,
            "rep_name": rep_name,
            "original_commission_paid": commission_paid,
            "days_active_before_cancel": days_active_before_cancel,
            "clawback_percentage": clawback_pct,
            "clawback_amount_due": clawback_amount,
            "net_commission_retained": net_retained,
            "clawback_policy_tier": "FULL_CLAWBACK_90D" if clawback_pct == 100.0 else "PARTIAL_CLAWBACK_180D" if clawback_pct == 50.0 else "ZERO_CLAWBACK_SAFE",
            "evaluated_at": datetime.now(timezone.utc).isoformat()
        }
""")

    # 2. backend/app/enterprise/sales_compensation/spiff_incentive_engine.py
    write_file("backend/app/enterprise/sales_compensation/spiff_incentive_engine.py", """from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class SPIFFIncentiveEngine:
    \"\"\"
    Special Performance Incentive Funds (SPIFFs):
    Calculates instant cash kickers for strategic product add-ons, multi-year prepayments, and competitive takeovers.
    \"\"\"
    @staticmethod
    def calculate_deal_spiffs(deal: Dict[str, Any]) -> Dict[str, Any]:
        deal_name = deal.get("name")
        val = float(deal.get("value", 0.0))
        is_multi_year = bool(deal.get("is_multi_year", False))
        is_competitive_rip = bool(deal.get("is_competitive_takeover", False))
        has_ai_copilot = bool(deal.get("has_ai_copilot_addon", False))

        earned_spiffs = []
        total_spiff_payout = 0.0

        if is_multi_year and val >= 50000.0:
            bonus = 2500.0
            earned_spiffs.append({"spiff_name": "Multi-Year Enterprise Commitment Bonus", "amount": bonus})
            total_spiff_payout += bonus

        if is_competitive_rip:
            bonus = 3000.0
            earned_spiffs.append({"spiff_name": "Legacy Competitor Takeover Bounty", "amount": bonus})
            total_spiff_payout += bonus

        if has_ai_copilot:
            bonus = 1000.0
            earned_spiffs.append({"spiff_name": "AI Copilot Strategic Adoption Kicker", "amount": bonus})
            total_spiff_payout += bonus

        return {
            "deal_name": deal_name,
            "deal_value": val,
            "earned_spiffs_count": len(earned_spiffs),
            "earned_spiffs_detail": earned_spiffs,
            "total_spiff_payout": total_spiff_payout,
            "disbursed_in_payroll_cycle": "NEXT_SCHEDULED_CYCLE"
        }
""")

    # 3. backend/app/enterprise/cpq_rules/multi_currency_fx_hedging_engine.py
    write_file("backend/app/enterprise/cpq_rules/multi_currency_fx_hedging_engine.py", """from typing import Any, Dict, List, Optional

class MultiCurrencyFXHedgingEngine:
    \"\"\"
    Multi-Currency CPQ Pricing & FX Volatility Buffer:
    Converts USD base quotes to EUR, GBP, JPY, AUD, CAD with automated 2.5% FX risk buffer.
    \"\"\"
    FX_SPOT_RATES = {
        "EUR": 0.92,
        "GBP": 0.78,
        "JPY": 155.40,
        "AUD": 1.52,
        "CAD": 1.36,
        "USD": 1.00
    }

    @classmethod
    def convert_and_hedge_quote(
        cls,
        usd_amount: float,
        target_currency: str,
        contract_term_years: int = 1
    ) -> Dict[str, Any]:
        curr = target_currency.upper()
        rate = cls.FX_SPOT_RATES.get(curr, 1.0)
        spot_converted = usd_amount * rate

        # FX volatility buffer (2.5% per term year)
        fx_buffer_pct = 2.5 * contract_term_years
        hedged_total = round(spot_converted * (1.0 + (fx_buffer_pct / 100.0)), 2)

        return {
            "base_usd_amount": usd_amount,
            "target_currency": curr,
            "spot_exchange_rate": rate,
            "spot_converted_amount": round(spot_converted, 2),
            "term_years": contract_term_years,
            "fx_volatility_buffer_pct": fx_buffer_pct,
            "final_hedged_local_currency_quote": hedged_total,
            "currency_symbol": "€" if curr == "EUR" else "£" if curr == "GBP" else "¥" if curr == "JPY" else "$"
        }
""")

    # 4. backend/app/enterprise/bi_cubes/funnel_micro_conversion_cube.py
    write_file("backend/app/enterprise/bi_cubes/funnel_micro_conversion_cube.py", """from typing import Any, Dict, List, Optional

class FunnelMicroConversionCube:
    \"\"\"
    Multi-Dimensional Sales Funnel Micro-Conversion Cube:
    Analyzes step-by-step conversion probabilities:
    Visitor -> Lead -> MQL -> SQL -> Demo -> Proposal -> Closed-Won.
    \"\"\"
    @staticmethod
    def compute_funnel_health(stage_counts: Dict[str, int]) -> Dict[str, Any]:
        visitors = max(1, stage_counts.get("visitors", 10000))
        leads = stage_counts.get("leads", 500)
        mqls = stage_counts.get("mqls", 250)
        sqls = stage_counts.get("sqls", 100)
        demos = stage_counts.get("demos", 60)
        proposals = stage_counts.get("proposals", 30)
        won = stage_counts.get("closed_won", 12)

        v_to_l = round((leads / visitors) * 100.0, 2)
        l_to_m = round((mqls / max(1, leads)) * 100.0, 2)
        m_to_s = round((sqls / max(1, mqls)) * 100.0, 2)
        s_to_d = round((demos / max(1, sqls)) * 100.0, 2)
        d_to_p = round((proposals / max(1, demos)) * 100.0, 2)
        p_to_w = round((won / max(1, proposals)) * 100.0, 2)
        end_to_end = round((won / visitors) * 100.0, 3)

        return {
            "visitor_to_lead_pct": v_to_l,
            "lead_to_mql_pct": l_to_m,
            "mql_to_sql_pct": m_to_s,
            "sql_to_demo_pct": s_to_d,
            "demo_to_proposal_pct": d_to_p,
            "proposal_to_won_pct": p_to_w,
            "end_to_end_conversion_pct": end_to_end,
            "funnel_bottleneck": "MQL_TO_SQL_TRANSITION" if m_to_s < 40.0 else "DEMO_TO_PROPOSAL" if d_to_p < 50.0 else "HEALTHY_VELOCITY"
        }
""")

    # 5. frontend/src/enterprise/EnterpriseClawbackEngineStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseClawbackEngineStudio.tsx", """import React, { useState } from "react";
import { AlertCircle, DollarSign, ShieldCheck, CheckCircle2 } from "lucide-react";

export const EnterpriseClawbackEngineStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            Commission Clawback & Retention Governance Engine
          </h3>
          <p className="text-xs text-slate-400">Automated clawback calculation rules for early customer contract terminations</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Policy Active
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">0 - 90 Days Churn</span>
          <div className="text-2xl font-bold text-red-400">100% Clawback</div>
          <span className="text-[10px] text-slate-400">Full Unvested Commission Recovery</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">91 - 180 Days Churn</span>
          <div className="text-2xl font-bold text-amber-400">50% Clawback</div>
          <span className="text-[10px] text-slate-400">Partial Shared-Risk Offset</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">181+ Days Active</span>
          <div className="text-2xl font-bold text-emerald-400">0% Clawback</div>
          <span className="text-[10px] text-emerald-400">Fully Vested Commission</span>
        </div>
      </div>
    </div>
  );
};
""")

    # 6. frontend/src/enterprise/EnterpriseSPIFFIncentiveStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseSPIFFIncentiveStudio.tsx", """import React, { useState } from "react";
import { Award, Zap, DollarSign, CheckCircle2 } from "lucide-react";

export const EnterpriseSPIFFIncentiveStudio: React.FC = () => {
  const spiffs = [
    { name: "Legacy Competitor Takeover Bounty", amount: "$3,000", criteria: "Rip-and-replace of Salesforce or Dynamics" },
    { name: "Multi-Year Enterprise Commitment Bonus", amount: "$2,500", criteria: "3+ Year upfront prepaid agreement" },
    { name: "AI Copilot Strategic Adoption Kicker", amount: "$1,000", criteria: "Attaching AI Assistant to any >50 seat deal" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Zap className="w-5 h-5 text-amber-400" />
            Strategic Sales SPIFFs & Deal Acceleration Bounties
          </h3>
          <p className="text-xs text-slate-400">Real-time performance kickers rewarding multi-year commitments and competitive takeovers</p>
        </div>
      </div>

      <div className="space-y-3">
        {spiffs.map((s, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{s.name}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">{s.criteria}</div>
            </div>
            <div className="text-right">
              <span className="text-sm font-bold text-emerald-400">{s.amount} Cash Bonus</span>
              <span className="text-[10px] text-slate-500 block">Instant Payroll Add</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    print("RevOps suite part 9 created successfully.")

if __name__ == "__main__":
    run()
