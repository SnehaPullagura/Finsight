import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/sales_playbooks/executive_briefing_generator.py
    write_file("backend/app/enterprise/sales_playbooks/executive_briefing_generator.py", """from datetime import date
from typing import Any, Dict, List, Optional

class ExecutiveDealBriefingGenerator:
    @staticmethod
    def generate_deal_brief(
        deal: Dict[str, Any],
        company: Dict[str, Any],
        key_stakeholders: List[Dict[str, Any]],
        pricing_quote: Dict[str, Any],
        meddic_evaluation: Dict[str, Any]
    ) -> Dict[str, Any]:
        return {
            "deal_id": deal.get("id"),
            "deal_name": deal.get("name"),
            "deal_value": float(deal.get("value", 0.0)),
            "probability": int(deal.get("probability", 50)),
            "target_close_date": deal.get("expected_close_date", date.today().isoformat()),
            "company_summary": {
                "name": company.get("name"),
                "industry": company.get("industry"),
                "annual_revenue": company.get("annual_revenue"),
                "tier": company.get("tier", "growth")
            },
            "stakeholders_count": len(key_stakeholders),
            "pricing_summary": {
                "list_price": pricing_quote.get("subtotal", 0.0),
                "discount_percentage": pricing_quote.get("discount_percentage", 0.0),
                "net_contract_value": pricing_quote.get("total_amount", 0.0)
            },
            "qualification_health": {
                "meddic_score": meddic_evaluation.get("total_meddic_score", 0),
                "level": meddic_evaluation.get("qualification_level", "Unqualified")
            },
            "generated_at": date.today().isoformat()
        }
""")

    # 2. backend/app/enterprise/crm_workflows/sla_auto_remediation_service.py
    write_file("backend/app/enterprise/crm_workflows/sla_auto_remediation_service.py", """from typing import Any, Dict, List, Optional

class SLAAutoRemediationService:
    @staticmethod
    def remediate_breached_ticket(ticket: Dict[str, Any], team_members: List[Dict[str, Any]]) -> Dict[str, Any]:
        tid = ticket.get("id")
        priority = (ticket.get("priority") or "medium").lower()

        # Elevate priority if not already critical
        new_priority = "critical" if priority in ["high", "medium"] else priority
        
        # Pick senior support engineer
        senior_engineers = [m for m in team_members if m.get("level") in ["Senior", "Lead", "Principal"]]
        assigned_to = senior_engineers[0] if senior_engineers else (team_members[0] if team_members else {})

        return {
            "ticket_id": tid,
            "previous_priority": priority,
            "escalated_priority": new_priority,
            "reassigned_to_id": assigned_to.get("id"),
            "reassigned_to_name": assigned_to.get("name"),
            "notification_action": "DISPATCH_URGENT_SLACK_ESCALATION",
            "remediation_status": "remediated"
        }
""")

    # 3. frontend/src/enterprise/EnterpriseObjectionBattlecards.tsx
    write_file("frontend/src/enterprise/EnterpriseObjectionBattlecards.tsx", """import React, { useState } from "react";
import { ShieldAlert, BookOpen, CheckCircle2, FileText, ChevronRight } from "lucide-react";

export const EnterpriseObjectionBattlecards: React.FC = () => {
  const cards = [
    {
      title: "Price Objection / Budget Tightness",
      category: "Pricing",
      talkingPoints: [
        "Present 3-year Total Cost of Ownership (TCO) advantage vs Salesforce / HubSpot",
        "Demonstrate 4.5 hours saved per sales rep per week via automated workflows",
        "Offer flexible quarterly ramp billing structure"
      ]
    },
    {
      title: "Competitor Comparison: Salesforce Enterprise",
      category: "Competitor Displacement",
      talkingPoints: [
        "100% native multi-tenant data isolation with zero shared-tenant leakage",
        "Includes full CPQ, AI Copilot, and DAG Workflows without expensive tier add-ons",
        "2-week rapid deployment vs 6-9 months typical implementation timeline"
      ]
    }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-emerald-400" />
            Sales Objection & Competitor Battlecards
          </h3>
          <p className="text-xs text-slate-400">Battle-tested responses, objection handling frameworks, and architectural differentiators</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {cards.map((card, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-5 rounded-xl space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-white">{card.title}</span>
              <span className="text-[10px] bg-slate-800 text-purple-400 px-2 py-0.5 rounded uppercase font-semibold">{card.category}</span>
            </div>
            <ul className="space-y-2 text-xs text-slate-300">
              {card.talkingPoints.map((tp, i) => (
                <li key={i} className="flex items-start gap-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0 mt-0.5" />
                  <span>{tp}</span>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    # 4. frontend/src/enterprise/EnterpriseExecutiveDealBrief.tsx
    write_file("frontend/src/enterprise/EnterpriseExecutiveDealBrief.tsx", """import React, { useState } from "react";
import { FileText, Building, DollarSign, Users, Award, ShieldCheck, CheckCircle2 } from "lucide-react";

export const EnterpriseExecutiveDealBrief: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <FileText className="w-5 h-5 text-emerald-400" />
            Executive Deal Brief & Sign-Off Packet
          </h3>
          <p className="text-xs text-slate-400">Automated deal memorandum for CRO and Finance executive review</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Approved for Signature
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase">Opportunity</span>
          <div className="text-sm font-bold text-white">Stark Industries — Global License</div>
          <span className="text-xs text-emerald-400 font-semibold">$250,000 Total Value</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase">Pricing Guardrails</span>
          <div className="text-sm font-bold text-white">10% Volume Discount Applied</div>
          <span className="text-xs text-slate-400">Within Standard Margin Band</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase">MEDDIC Qualification</span>
          <div className="text-sm font-bold text-emerald-400">Score: 90 / 100</div>
          <span className="text-xs text-slate-400">Economic Buyer & Champion Confirmed</span>
        </div>
      </div>
    </div>
  );
};
""")

    print("Created briefing generator, SLA remediation, battlecards, and executive brief UI.")

if __name__ == '__main__':
    run()
