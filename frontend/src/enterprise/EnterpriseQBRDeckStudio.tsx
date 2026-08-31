import React, { useState } from "react";
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
