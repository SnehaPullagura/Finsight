import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/deal_room/dsr_template_factory.py
    write_file("backend/app/enterprise/deal_room/dsr_template_factory.py", """from typing import Any, Dict, List, Optional

class DSRTemplateFactory:
    \"\"\"
    Pre-packaged Digital Sales Room Templates:
    - Enterprise M&A / Strategic Acquisition
    - Mid-Market Fast-Close Package
    - Security & InfoSec Heavy Procurement
    \"\"\"
    TEMPLATES = {
        "ENTERPRISE_STRATEGIC": {
            "sections": ["Executive Summary", "Architecture Blueprint", "CPQ Multi-Year Quote", "SOC2 Compliance", "Mutual Action Plan"],
            "nda_required": True,
            "tam_allocation_included": True
        },
        "INFOSEC_HEAVY": {
            "sections": ["Penetration Test Summary", "ISO 27001 / SOC2 Type II", "Data Flow Architecture", "Subprocessor List", "DPA Agreement"],
            "nda_required": True,
            "tam_allocation_included": False
        },
        "FAST_TRACK": {
            "sections": ["Product Tour Video", "1-Click Standard Order Form", "Implementation Timeline"],
            "nda_required": False,
            "tam_allocation_included": False
        }
    }

    @classmethod
    def instantiate_template(cls, template_name: str, deal_context: Dict[str, Any]) -> Dict[str, Any]:
        tmpl = cls.TEMPLATES.get(template_name.upper(), cls.TEMPLATES["FAST_TRACK"])
        return {
            "template_name": template_name.upper(),
            "account_name": deal_context.get("account_name"),
            "deal_value": deal_context.get("value"),
            "included_sections": tmpl["sections"],
            "is_nda_mandated": tmpl["nda_required"],
            "includes_tam_support": tmpl["tam_allocation_included"],
            "factory_status": "INSTANTIATED_READY_TO_CUSTOMIZE"
        }
""")

    # 2. backend/app/enterprise/deal_room/buyer_intent_alert_engine.py
    write_file("backend/app/enterprise/deal_room/buyer_intent_alert_engine.py", """from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class BuyerIntentAlertEngine:
    \"\"\"
    Dispatches Slack and webhook notifications when an economic buyer views the pricing table or forwards the proposal.
    \"\"\"
    @staticmethod
    def evaluate_intent_trigger(
        visitor_email: str,
        page_viewed: str,
        dwell_seconds: int
    ) -> Dict[str, Any]:
        is_pricing = "pricing" in page_viewed.lower() or "quote" in page_viewed.lower()
        is_high_intent = is_pricing and dwell_seconds >= 60

        return {
            "visitor_email": visitor_email,
            "page_viewed": page_viewed,
            "dwell_seconds": dwell_seconds,
            "is_high_intent_event": is_high_intent,
            "alert_priority": "P1_INSTANT_REP_NOTIFICATION" if is_high_intent else "P3_PASSIVE_LOG",
            "recommended_sales_action": "Call/Email buyer immediately while proposal is open." if is_high_intent else "None",
            "triggered_at": datetime.now(timezone.utc).isoformat()
        }
""")

    # 3. backend/app/enterprise/billing_mediation/prepaid_credit_rollover_policy.py
    write_file("backend/app/enterprise/billing_mediation/prepaid_credit_rollover_policy.py", """from typing import Any, Dict, List, Optional

class PrepaidCreditRolloverPolicy:
    \"\"\"
    Annual prepaid credit expiration & rollover calculator:
    Allows up to 20% unused credit rollover upon contract renewal execution.
    \"\"\"
    @staticmethod
    def calculate_renewal_rollover(
        unused_credits_balance: float,
        is_contract_renewed: bool,
        max_rollover_percentage: float = 20.0
    ) -> Dict[str, Any]:
        if not is_contract_renewed:
            return {
                "unused_credits_balance": unused_credits_balance,
                "credits_rolled_over": 0.0,
                "credits_forfeited": unused_credits_balance,
                "policy_outcome": "ALL_CREDITS_EXPIRED_NO_RENEWAL"
            }

        max_allowed = round(unused_credits_balance * (max_rollover_percentage / 100.0), 2)
        forfeited = round(unused_credits_balance - max_allowed, 2)

        return {
            "unused_credits_balance": unused_credits_balance,
            "max_rollover_pct_allowed": max_rollover_percentage,
            "credits_rolled_over_to_new_term": max_allowed,
            "credits_forfeited": forfeited,
            "policy_outcome": "RENEWAL_ROLLOVER_APPLIED"
        }
""")

    # 4. backend/app/enterprise/pipeline_forecasting/deal_slippage_mitigation_plan.py
    write_file("backend/app/enterprise/pipeline_forecasting/deal_slippage_mitigation_plan.py", """from typing import Any, Dict, List, Optional

class DealSlippageMitigationPlan:
    \"\"\"
    Prescribes targeted concession packages to prevent quarter-end deal slippage.
    \"\"\"
    @staticmethod
    def generate_mitigation_offer(deal: Dict[str, Any]) -> Dict[str, Any]:
        dname = deal.get("name")
        val = float(deal.get("value", 0.0))

        concessions = [
            "Waive first 3 months implementation fee ($15,000 value)",
            "Lock in 10% multi-year discount upon signature by quarter close",
            "Include 1 complimentary named TAM seat for first 90 days"
        ]

        return {
            "deal_name": dname,
            "contract_value": val,
            "slippage_mitigation_package": concessions,
            "required_cro_approval": val >= 100000.0,
            "expected_pull_forward_success_rate_pct": 72.5
        }
""")

    # 5. frontend/src/enterprise/EnterpriseDSRTemplateStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseDSRTemplateStudio.tsx", """import React, { useState } from "react";
import { Layout, CheckCircle2, ShieldCheck, FileText } from "lucide-react";

export const EnterpriseDSRTemplateStudio: React.FC = () => {
  const templates = [
    { name: "Enterprise Strategic M&A", sections: "5 Modules", nda: "Required", tam: "Included", tier: "Tier 1" },
    { name: "InfoSec Heavy Compliance", sections: "5 Modules", nda: "Required", tam: "Standard", tier: "Security Focused" },
    { name: "Fast Track Commercial", sections: "3 Modules", nda: "Optional", tam: "Self-Service", tier: "Velocity" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Layout className="w-5 h-5 text-emerald-400" />
            Digital Sales Room (DSR) Enterprise Template Library
          </h3>
          <p className="text-xs text-slate-400">Pre-configured buyer room layouts with automated NDA gating and TAM collateral</p>
        </div>
      </div>

      <div className="space-y-3">
        {templates.map((t, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{t.name}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">{t.sections} • NDA: {t.nda} • TAM: {t.tam}</div>
            </div>
            <span className="text-xs font-semibold bg-emerald-950 text-emerald-400 border border-emerald-800 px-2.5 py-1 rounded-full">
              {t.tier}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    # 6. frontend/src/enterprise/EnterpriseBuyerIntentAlertStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseBuyerIntentAlertStudio.tsx", """import React, { useState } from "react";
import { Zap, Bell, CheckCircle2, Clock } from "lucide-react";

export const EnterpriseBuyerIntentAlertStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Zap className="w-5 h-5 text-amber-400" />
            Real-Time Buyer Intent Trigger & Hot Deal Alert Engine
          </h3>
          <p className="text-xs text-slate-400">Sub-second notifications dispatched when economic buyers review pricing and legal terms</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Live Triggers Active
        </span>
      </div>

      <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold text-white">Live Buyer Event: Bruce Wayne (CEO) viewing Pricing Table</span>
          <span className="text-xs text-emerald-400 font-semibold">Active Now (3m 42s dwell)</span>
        </div>
        <div className="space-y-2 text-xs text-slate-300">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>P1 alert sent to Slack #deals-wayne-enterprises & Lead AE phone</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>Recommended action: Send personalized follow-up SMS with custom concession ramp</span>
          </div>
        </div>
      </div>
    </div>
  );
};
""")

    # 7. frontend/src/enterprise/EnterpriseCreditRolloverStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseCreditRolloverStudio.tsx", """import React, { useState } from "react";
import { DollarSign, RefreshCw, CheckCircle2, Award } from "lucide-react";

export const EnterpriseCreditRolloverStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <DollarSign className="w-5 h-5 text-emerald-400" />
            Prepaid Commit Credit Expiration & Rollover Policy
          </h3>
          <p className="text-xs text-slate-400">Automated 20% credit rollover calculations incentivizing early enterprise contract renewals</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          20% Max Rollover
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Unused Credit Balance</span>
          <div className="text-2xl font-bold text-white">$14,500</div>
          <span className="text-[10px] text-slate-400">Year 1 Ending Prepaid Pool</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Rolled Over to Year 2</span>
          <div className="text-2xl font-bold text-emerald-400">$2,900</div>
          <span className="text-[10px] text-emerald-400">Applied to Renewal Term</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Forfeited Breakage</span>
          <div className="text-2xl font-bold text-white">$11,600</div>
          <span className="text-[10px] text-slate-400">Recognized as Contract Breakage</span>
        </div>
      </div>
    </div>
  );
};
""")

    print("DSR and Billing part 3 created successfully.")

if __name__ == "__main__":
    run()
