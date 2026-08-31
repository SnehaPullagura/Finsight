import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/executive_sales_rep_pipeline_generation_velocity.py
    write_file("backend/app/enterprise/crm_analytics/executive_sales_rep_pipeline_generation_velocity.py", """from typing import Any, Dict, List, Optional
from collections import defaultdict

class RepPipelineGenerationVelocityAnalyzer:
    @staticmethod
    def calculate_pipeline_created(reps_sourcing: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for r in reps_sourcing:
            name = r.get("rep_name")
            pipe_created = float(r.get("pipeline_dollars_created", 0.0))
            quota = float(r.get("quarterly_quota", 250000.0))
            self_sourced_pct = float(r.get("self_sourced_pct", 50.0))

            pipeline_multiple = round(pipe_created / max(1.0, quota), 2)
            tier = "High Pipeline Engine (> 4x)" if pipeline_multiple >= 4.0 else "Self-Sustaining (3x - 4x)" if pipeline_multiple >= 3.0 else "Dependent on Inbound (< 3x)"

            results.append({
                "rep_name": name,
                "pipeline_created": pipe_created,
                "quarterly_quota": quota,
                "pipeline_created_multiple": pipeline_multiple,
                "self_sourced_percentage": self_sourced_pct,
                "sourcing_efficiency_tier": tier
            })

        return sorted(results, key=lambda x: x["pipeline_created_multiple"], reverse=True)
""")

    # 2. backend/app/enterprise/customer_success/health_score_ai_qbr_generator.py
    write_file("backend/app/enterprise/customer_success/health_score_ai_qbr_generator.py", """from typing import Any, Dict, List, Optional

class AIQBRDeckGenerator:
    @staticmethod
    def generate_qbr_briefing(company: Dict[str, Any], usage_metrics: Dict[str, Any]) -> Dict[str, Any]:
        cname = company.get("name")
        total_sessions = usage_metrics.get("total_sessions_qtr", 12000)
        time_saved_hours = round(total_sessions * 0.25, 1)

        return {
            "account_name": cname,
            "qbr_period": "Q3 2026",
            "business_impact_metrics": {
                "total_platform_sessions": total_sessions,
                "estimated_sales_hours_saved": time_saved_hours,
                "workflow_automations_executed": usage_metrics.get("automations_executed", 850),
                "proposals_generated": usage_metrics.get("proposals_count", 140)
            },
            "recommendations_for_next_quarter": [
                "Deploy CPQ Rule Configurator for custom bundles",
                "Integrate SSO SCIM automated user provisioning",
                "Activate AI Copilot automated meeting summaries"
            ],
            "readiness_status": "READY_FOR_EXECUTIVE_PRESENTATION"
        }
""")

    # 3. frontend/src/enterprise/EnterprisePipelineGenVelocityStudio.tsx
    write_file("frontend/src/enterprise/EnterprisePipelineGenVelocityStudio.tsx", """import React, { useState } from "react";
import { TrendingUp, Users, Target, CheckCircle2 } from "lucide-react";

export const EnterprisePipelineGenVelocityStudio: React.FC = () => {
  const reps = [
    { name: "Alex Vance", created: "$950,000", quota: "$250,000", multiple: "3.8x", selfSourced: "65%", tier: "Self-Sustaining" },
    { name: "Sarah Connor", created: "$1,200,000", quota: "$250,000", multiple: "4.8x", selfSourced: "72%", tier: "High Engine" },
    { name: "John Wick", created: "$540,000", quota: "$250,000", multiple: "2.1x", selfSourced: "30%", tier: "Inbound Dependent" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Target className="w-5 h-5 text-emerald-400" />
            Sales Rep Outbound Pipeline Generation Velocity
          </h3>
          <p className="text-xs text-slate-400">Quarterly new pipeline creation multiple and self-sourced outbound ratio</p>
        </div>
      </div>

      <div className="space-y-3">
        {reps.map((r, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{r.name}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Created: {r.created} • Self-Sourced: {r.selfSourced}</div>
            </div>
            <div className="text-right">
              <span className="text-sm font-bold text-emerald-400">{r.multiple} Quota Coverage</span>
              <span className="text-[10px] text-slate-500 block">{r.tier}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    # 4. frontend/src/enterprise/EnterpriseQBRDeckStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseQBRDeckStudio.tsx", """import React, { useState } from "react";
import { FileText, CheckCircle2, Award, Sparkles, TrendingUp } from "lucide-react";

export const EnterpriseQBRDeckStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-emerald-400" />
            AI Automated Quarterly Business Review (QBR) Generator
          </h3>
          <p className="text-xs text-slate-400">One-click synthesis of business value delivered, time saved, and roadmap priorities</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          QBR Ready
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Total Sessions</span>
          <div className="text-2xl font-bold text-white">12,450</div>
          <span className="text-[10px] text-emerald-400">99.2% Team Adoption</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Hours Saved</span>
          <div className="text-2xl font-bold text-emerald-400">3,112 Hrs</div>
          <span className="text-[10px] text-slate-400">Automated CRM Workflows</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Automations Run</span>
          <div className="text-2xl font-bold text-white">850 DAGs</div>
          <span className="text-[10px] text-emerald-400">100% Success Rate</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Proposals Created</span>
          <div className="text-2xl font-bold text-white">140 Quotes</div>
          <span className="text-[10px] text-emerald-400">$4.2M Quoted</span>
        </div>
      </div>
    </div>
  );
};
""")

    print("Created pipeline gen velocity, QBR generator, and UI studios.")

if __name__ == '__main__':
    run()
