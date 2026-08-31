import React, { useState } from "react";
import { Play, CheckCircle2, Shield, HeartPulse, ArrowRight } from "lucide-react";

export const EnterpriseCSInterventionWorkflow: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <HeartPulse className="w-5 h-5 text-emerald-400" />
            Customer Success Escalation & Intervention Workflow
          </h3>
          <p className="text-xs text-slate-400">Automated triage routing and recovery milestone tracking</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          CS Workflow Active
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Step 1: Automated Detection</span>
          <div className="text-xs font-bold text-white">Telemetry Risk Triggered</div>
          <span className="text-[10px] text-emerald-400">&lt; 15% DAU/MAU</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Step 2: Executive Alert</span>
          <div className="text-xs font-bold text-white">Slack & Email Notification</div>
          <span className="text-[10px] text-emerald-400">Assigned Senior CSM</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Step 3: Recovery Sprint</span>
          <div className="text-xs font-bold text-white">Mutual Success Plan</div>
          <span className="text-[10px] text-emerald-400">Target: 85+ Health</span>
        </div>
      </div>
    </div>
  );
};
