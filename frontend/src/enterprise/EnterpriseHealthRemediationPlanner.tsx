import React, { useState } from "react";
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
