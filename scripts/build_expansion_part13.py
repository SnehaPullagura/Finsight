import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_workflows/contract_renewal_engine.py
    write_file("backend/app/enterprise/crm_workflows/contract_renewal_engine.py", """from datetime import date, timedelta
from typing import Any, Dict, List, Optional

class EnterpriseContractRenewalEngine:
    @staticmethod
    def calculate_auto_renewal_terms(
        contract: Dict[str, Any],
        standard_uplift_pct: float = 5.0,
        extend_years: int = 1
    ) -> Dict[str, Any]:
        curr_end_str = contract.get("termination_date") or date.today().isoformat()
        curr_end = date.fromisoformat(curr_end_str)
        curr_val = float(contract.get("contract_value", {}).get("total_amount", 0.0))

        new_val = round(curr_val * (1.0 + (standard_uplift_pct / 100.0)), 2)
        new_end = curr_end + timedelta(days=365 * extend_years)

        return {
            "original_contract_id": contract.get("id"),
            "renewal_effective_date": curr_end.isoformat(),
            "new_termination_date": new_end.isoformat(),
            "previous_annual_value": curr_val,
            "uplift_percentage": standard_uplift_pct,
            "new_annual_value": new_val,
            "auto_renew_status": "drafted"
        }
""")

    # 2. backend/app/enterprise/crm_workflows/omnichannel_routing_manager.py
    write_file("backend/app/enterprise/crm_workflows/omnichannel_routing_manager.py", """from typing import Any, Dict, List, Optional

class OmnichannelRoutingManager:
    @staticmethod
    def select_best_channel(contact_preferences: Dict[str, Any], message_urgency: str) -> str:
        if message_urgency.lower() == "critical":
            return "sms" if contact_preferences.get("phone") else "email"
        elif contact_preferences.get("prefers_slack"):
            return "slack"
        elif contact_preferences.get("prefers_whatsapp"):
            return "whatsapp"
        return "email"
""")

    # 3. frontend/src/enterprise/EnterpriseWorkflowVisualizer.tsx
    write_file("frontend/src/enterprise/EnterpriseWorkflowVisualizer.tsx", """import React, { useState } from "react";
import { GitBranch, Play, CheckCircle2, Clock, AlertTriangle, ArrowDown } from "lucide-react";

export const EnterpriseWorkflowVisualizer: React.FC = () => {
  const steps = [
    { id: "1", title: "Trigger: Inbound Enterprise Lead Created", type: "trigger", status: "completed" },
    { id: "2", title: "Condition: Annual Revenue >= $10,000,000", type: "condition", status: "completed" },
    { id: "3", title: "Action: Auto-Assign to Strategic SDR Team", type: "action", status: "completed" },
    { id: "4", title: "Action: Dispatch Slack Alert to #sales-urgent", type: "action", status: "completed" },
    { id: "5", title: "Action: Schedule 15-Min SLA Escalation Timer", type: "action", status: "running" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <GitBranch className="w-5 h-5 text-emerald-400" />
            DAG Workflow Automation Visualizer
          </h3>
          <p className="text-xs text-slate-400">Directed Acyclic Graph visual execution trace for real-time CRM lifecycle automations</p>
        </div>
      </div>

      <div className="space-y-3 max-w-lg mx-auto py-4">
        {steps.map((step, idx) => (
          <React.Fragment key={step.id}>
            <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between shadow">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-slate-900 border border-slate-700 flex items-center justify-center text-xs font-bold text-slate-300">
                  {step.id}
                </div>
                <div>
                  <div className="text-xs font-bold text-white">{step.title}</div>
                  <div className="text-[10px] text-slate-500 uppercase">{step.type}</div>
                </div>
              </div>
              <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${
                step.status === "completed" ? "bg-emerald-950 text-emerald-400 border border-emerald-800" : "bg-blue-950 text-blue-400 border border-blue-800"
              }`}>
                {step.status}
              </span>
            </div>
            {idx < steps.length - 1 && (
              <div className="flex justify-center text-slate-600">
                <ArrowDown className="w-4 h-4" />
              </div>
            )}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
};
""")

    # 4. frontend/src/enterprise/EnterpriseFormBuilderStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseFormBuilderStudio.tsx", """import React, { useState } from "react";
import { LayoutGrid, Plus, Trash2, Eye, Save } from "lucide-react";

export const EnterpriseFormBuilderStudio: React.FC = () => {
  const [fields, setFields] = useState([
    { id: "1", label: "Estimated Annual Budget", type: "Currency", required: true },
    { id: "2", label: "Executive Decision Maker", type: "Lookup (Contact)", required: true },
    { id: "3", label: "Contract Target Go-Live Date", type: "Date", required: false },
    { id: "4", label: "Competitive Landscape", type: "Multi-Select Picklist", required: false }
  ]);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <LayoutGrid className="w-5 h-5 text-emerald-400" />
            Dynamic CRM Layout & Schema Builder
          </h3>
          <p className="text-xs text-slate-400">Design custom object layouts, validation rules, and dependent fields</p>
        </div>
        <button className="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-500 text-white px-3 py-1.5 rounded-lg text-xs font-semibold shadow-lg transition-colors">
          <Save className="w-4 h-4" />
          Save Form Layout
        </button>
      </div>

      <div className="space-y-3">
        {fields.map(f => (
          <div key={f.id} className="bg-slate-950 border border-slate-800 p-3 rounded-lg flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{f.label}</div>
              <div className="text-[10px] text-slate-500">{f.type} {f.required && "• Required"}</div>
            </div>
            <span className="text-xs text-emerald-400 font-medium">Active</span>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    print("Created renewal engine, omnichannel router, workflow visualizer, and form builder.")

if __name__ == '__main__':
    run()
