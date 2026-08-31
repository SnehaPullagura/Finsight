import React, { useState } from "react";
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
