import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/executive_kpi_scorecard.py
    write_file("backend/app/enterprise/crm_analytics/executive_kpi_scorecard.py", """from typing import Any, Dict, List, Optional

class ExecutiveKPIScorecard:
    @staticmethod
    def calculate_saas_metrics(
        starting_arr: float,
        ending_arr: float,
        free_cash_flow_margin_pct: float,
        sales_and_marketing_spend: float,
        net_new_arr_added: float,
        average_customer_cac: float,
        average_customer_ltv: float
    ) -> Dict[str, Any]:
        arr_growth_pct = round(((ending_arr - starting_arr) / max(1.0, starting_arr)) * 100.0, 1)
        
        # Rule of 40: Growth Rate % + Free Cash Flow Margin %
        rule_of_40_score = round(arr_growth_pct + free_cash_flow_margin_pct, 1)

        # SaaS Magic Number: Net New ARR / S&M Spend
        magic_number = round(net_new_arr_added / max(1.0, sales_and_marketing_spend), 2)

        # LTV to CAC Ratio
        ltv_cac_ratio = round(average_customer_ltv / max(1.0, average_customer_cac), 2)

        return {
            "arr_growth_percentage": arr_growth_pct,
            "free_cash_flow_margin": free_cash_flow_margin_pct,
            "rule_of_40_score": rule_of_40_score,
            "is_rule_of_40_achieved": rule_of_40_score >= 40.0,
            "magic_number": magic_number,
            "magic_number_health": "Top Tier" if magic_number >= 1.0 else "Good" if magic_number >= 0.75 else "Needs Efficiency",
            "ltv_to_cac_ratio": ltv_cac_ratio,
            "benchmark_status": "World Class SaaS" if rule_of_40_score >= 40.0 and ltv_cac_ratio >= 3.0 else "Healthy Growth"
        }
""")

    # 2. backend/app/enterprise/sales_playbooks/deal_approval_escalation_engine.py
    write_file("backend/app/enterprise/sales_playbooks/deal_approval_escalation_engine.py", """from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

class DealApprovalEscalationEngine:
    @staticmethod
    def check_pending_approvals(pending_quotes: List[Dict[str, Any]], max_wait_hours: int = 24) -> List[Dict[str, Any]]:
        escalations = []
        now = datetime.now(timezone.utc)

        for q in pending_quotes:
            submitted_str = q.get("submitted_at")
            if not submitted_str:
                continue
            submitted_time = datetime.fromisoformat(submitted_str.replace("Z", "+00:00"))
            hours_elapsed = (now - submitted_time).total_seconds() / 3600.0

            if hours_elapsed >= max_wait_hours:
                escalations.append({
                    "quote_id": q.get("id"),
                    "deal_name": q.get("deal_name"),
                    "amount": q.get("total_amount"),
                    "hours_elapsed": round(hours_elapsed, 1),
                    "current_approver_role": q.get("current_approver_role", "Sales Director"),
                    "escalate_to_role": "VP of Sales / CRO",
                    "action": "TRIGGER_EXECUTIVE_SLACK_ESCALATION"
                })

        return escalations
""")

    # 3. backend/app/enterprise/customer_success/health_score_remediation_planner.py
    write_file("backend/app/enterprise/customer_success/health_score_remediation_planner.py", """from typing import Any, Dict, List, Optional

class HealthScoreRemediationPlanner:
    @staticmethod
    def generate_intervention_play(company: Dict[str, Any], health_score: int, primary_failing_metric: str) -> Dict[str, Any]:
        cid = company.get("id")
        cname = company.get("name")

        playbooks = {
            "low_product_usage": {
                "action_title": "Product Re-Engagement & Feature Certification",
                "recommended_steps": [
                    "Audit unused license seats across customer teams",
                    "Conduct dedicated admin onboarding refresher workshop",
                    "Share personalized ROI workflow automation dashboard"
                ]
            },
            "support_ticket_backlog": {
                "action_title": "Technical Escalation & Bug Remediation Sprint",
                "recommended_steps": [
                    "Assign dedicated Tier 3 Support Engineer",
                    "Conduct daily standup on open blockers",
                    "Provide weekly executive status updates"
                ]
            },
            "detractor_nps": {
                "action_title": "Executive Alignment & Relationship Recovery",
                "recommended_steps": [
                    "Schedule VP-level listening session within 48 hours",
                    "Document mutual success plan with clear deliverable milestones",
                    "Offer roadmap influence on key requested enterprise features"
                ]
            }
        }

        play = playbooks.get(primary_failing_metric, playbooks["low_product_usage"])

        return {
            "company_id": cid,
            "company_name": cname,
            "current_health_score": health_score,
            "failing_metric": primary_failing_metric,
            "intervention_plan": play,
            "target_recovery_health_score": 85
        }
""")

    # 4. frontend/src/enterprise/EnterpriseExecutiveKPIScorecard.tsx
    write_file("frontend/src/enterprise/EnterpriseExecutiveKPIScorecard.tsx", """import React, { useState } from "react";
import { Award, TrendingUp, CheckCircle2, DollarSign, Target, Activity } from "lucide-react";

export const EnterpriseExecutiveKPIScorecard: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Award className="w-5 h-5 text-emerald-400" />
            Executive SaaS Performance Scorecard & Rule of 40
          </h3>
          <p className="text-xs text-slate-400">Board-level financial and operational efficiency metrics</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Top Decile SaaS
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Rule of 40 Index</span>
          <div className="text-2xl font-bold text-emerald-400">54.2%</div>
          <span className="text-[10px] text-slate-400">38.2% Growth + 16.0% FCF</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">SaaS Magic Number</span>
          <div className="text-2xl font-bold text-white">1.34x</div>
          <span className="text-[10px] text-emerald-400">High S&M Capital Efficiency</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">LTV : CAC Ratio</span>
          <div className="text-2xl font-bold text-white">4.8x</div>
          <span className="text-[10px] text-emerald-400">Industry Target: 3.0x+</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">CAC Payback Period</span>
          <div className="text-2xl font-bold text-white">9.2 Months</div>
          <span className="text-[10px] text-emerald-400">Top-Quartile Recovery</span>
        </div>
      </div>
    </div>
  );
};
""")

    # 5. frontend/src/enterprise/EnterpriseHealthRemediationPlanner.tsx
    write_file("frontend/src/enterprise/EnterpriseHealthRemediationPlanner.tsx", """import React, { useState } from "react";
import { AlertTriangle, CheckCircle2, Shield, ArrowRight, Play } from "lucide-react";

export const EnterpriseHealthRemediationPlanner: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-amber-400" />
            Customer Success Churn Prevention & Health Recovery Playbook
          </h3>
          <p className="text-xs text-slate-400">Automated intervention triggers for at-risk accounts with targeted recovery roadmaps</p>
        </div>
        <button className="bg-emerald-600 hover:bg-emerald-500 text-white px-3 py-1.5 rounded-lg text-xs font-semibold shadow transition-colors flex items-center gap-1.5">
          <Play className="w-3.5 h-3.5" />
          Deploy Intervention
        </button>
      </div>

      <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold text-white">Recommended Intervention: Product Re-Engagement & Feature Certification</span>
          <span className="text-xs text-amber-400 font-semibold">Target Health: 85+</span>
        </div>
        <div className="space-y-2 text-xs text-slate-300">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>Audit unused license seats across customer teams</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>Conduct dedicated admin onboarding refresher workshop</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>Share personalized ROI workflow automation dashboard</span>
          </div>
        </div>
      </div>
    </div>
  );
};
""")

    print("Created executive scorecard, escalation engine, remediation planner, and UI suites.")

if __name__ == '__main__':
    run()
