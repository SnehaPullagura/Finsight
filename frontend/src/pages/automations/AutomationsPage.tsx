import React, { useEffect, useState } from "react";
import { Workflow, PlayCircle } from "lucide-react";
import { api } from "../../services/api";
import { AutomationWorkflow } from "../../types";

export const AutomationsPage: React.FC = () => {
  const [workflows, setWorkflows] = useState<AutomationWorkflow[]>([]);

  useEffect(() => {
    api.getWorkflows().then(res => setWorkflows(res.data)).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-900">Workflow Automation Engine</h1>
        <p className="text-xs text-slate-500">Event-driven triggers, conditional logic trees, and automated task actions</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {workflows.map(w => (
          <div key={w.id} className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs space-y-3">
            <div className="flex justify-between items-start">
              <h4 className="text-xs font-bold text-slate-900">{w.name}</h4>
              <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-100 text-emerald-800">Active</span>
            </div>
            <div className="text-xs text-slate-600 bg-slate-50 p-2.5 rounded border border-slate-100 font-mono text-[11px]">
              When: {w.trigger_event} ➔ Then: {w.actions.length} Actions
            </div>
          </div>
        ))}
        {workflows.length === 0 && <div className="p-8 col-span-full text-center text-xs text-slate-400 bg-white rounded-xl border border-slate-200">Workflows active in background engine.</div>}
      </div>
    </div>
  );
};
