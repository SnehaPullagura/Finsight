import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/executive_sales_pipeline_slippage_prevention.py
    write_file("backend/app/enterprise/crm_analytics/executive_sales_pipeline_slippage_prevention.py", """from typing import Any, Dict, List, Optional

class SlippagePreventionPlaybookEngine:
    @staticmethod
    def prescribe_prevention_play(deal: Dict[str, Any], slippage_risk_score: int) -> Dict[str, Any]:
        dname = deal.get("name")
        val = float(deal.get("value", 0.0))

        if slippage_risk_score >= 70:
            actions = [
                "Schedule immediate CRO-to-CEO peer negotiation sync",
                "Offer customized payment schedule ramp",
                "Dispatch technical solutions engineer for immediate security review sign-off"
            ]
        elif slippage_risk_score >= 40:
            actions = [
                "Conduct champion check-in call within 24 hours",
                "Send executive summary briefing deck to economic buyer"
            ]
        else:
            actions = ["Maintain standard sales cadence"]

        return {
            "deal_name": dname,
            "deal_value": val,
            "risk_score": slippage_risk_score,
            "prescribed_intervention_actions": actions,
            "is_executive_escalation_triggered": slippage_risk_score >= 70
        }
""")

    # 2. backend/app/enterprise/customer_success/health_score_expansion_opportunity_digest.py
    write_file("backend/app/enterprise/customer_success/health_score_expansion_opportunity_digest.py", """from typing import Any, Dict, List, Optional

class ExpansionOpportunityDigestBuilder:
    @staticmethod
    def build_weekly_digest(expansion_candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_potential_arr = sum(float(c.get("projected_expansion_arr", 0.0)) for c in expansion_candidates)
        top_candidates = sorted(expansion_candidates, key=lambda x: float(x.get("projected_expansion_arr", 0.0)), reverse=True)[:5]

        return {
            "digest_title": "Weekly Customer Success Expansion & Upsell Intelligence Digest",
            "total_qualified_expansion_accounts": len(expansion_candidates),
            "total_addressable_expansion_pipeline": round(total_potential_arr, 2),
            "top_expansion_opportunities": top_candidates,
            "digest_generated_status": "READY_FOR_SLACK_AND_EMAIL_DISPATCH"
        }
""")

    # 3. frontend/src/enterprise/EnterprisePipelineSlippagePreventionStudio.tsx
    write_file("frontend/src/enterprise/EnterprisePipelineSlippagePreventionStudio.tsx", """import React, { useState } from "react";
import { ShieldAlert, TrendingDown, CheckCircle2, DollarSign, Play } from "lucide-react";

export const EnterprisePipelineSlippagePreventionStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-amber-400" />
            Deal Slippage Auto-Remediation Playbook
          </h3>
          <p className="text-xs text-slate-400">Automated intervention blueprints triggered when enterprise deal velocity stagnates</p>
        </div>
        <button className="flex items-center gap-2 bg-amber-600 hover:bg-amber-500 text-white px-3 py-1.5 rounded-lg text-xs font-semibold shadow transition-colors">
          <Play className="w-4 h-4" />
          Deploy Intervention
        </button>
      </div>

      <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold text-white">Target Opportunity: Wayne Enterprises Global MSA ($250,000)</span>
          <span className="text-xs text-amber-400 font-semibold">Risk: 78 / 100</span>
        </div>
        <div className="space-y-2 text-xs text-slate-300">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>Schedule immediate CRO-to-CEO peer negotiation sync</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>Offer customized payment schedule ramp</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>Dispatch technical solutions engineer for immediate security review sign-off</span>
          </div>
        </div>
      </div>
    </div>
  );
};
""")

    # 4. frontend/src/enterprise/EnterpriseExpansionDigestStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseExpansionDigestStudio.tsx", """import React, { useState } from "react";
import { Mail, TrendingUp, CheckCircle2, DollarSign } from "lucide-react";

export const EnterpriseExpansionDigestStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Mail className="w-5 h-5 text-emerald-400" />
            Weekly CS Expansion & Upsell Intelligence Digest
          </h3>
          <p className="text-xs text-slate-400">Executive email summary of qualified high-health expansion opportunities</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Digest Active
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Expansion Opportunities</span>
          <div className="text-2xl font-bold text-white">14 Accounts</div>
          <span className="text-[10px] text-slate-400">Health 85+ with 90%+ Seat Usage</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Total Potential Pipeline</span>
          <div className="text-2xl font-bold text-emerald-400">$640,000 ARR</div>
          <span className="text-[10px] text-emerald-400">+$45k Average Upsell ACV</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Auto-Sync Cadence</span>
          <div className="text-2xl font-bold text-white">Every Monday</div>
          <span className="text-[10px] text-slate-400">Slack #sales-leads & Email</span>
        </div>
      </div>
    </div>
  );
};
""")

    print("Created slippage prevention, expansion digest, and UI studios.")

if __name__ == '__main__':
    run()
