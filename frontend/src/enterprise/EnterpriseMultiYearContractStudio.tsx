import React, { useState } from "react";
import { FileText, ShieldCheck, CheckCircle2, DollarSign } from "lucide-react";

export const EnterpriseMultiYearContractStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <FileText className="w-5 h-5 text-emerald-400" />
            Multi-Year Enterprise Agreement Generator
          </h3>
          <p className="text-xs text-slate-400">Automated legal contract drafting with co-termed commitments and SLA schedules</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Draft Ready
        </span>
      </div>

      <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold text-white">Target Account: Wayne Enterprises (3-Year Master Services Agreement)</span>
          <span className="text-xs text-emerald-400 font-semibold">$247,500 TCV</span>
        </div>
        <div className="space-y-2 text-xs text-slate-300">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>36-Month non-cancellable enterprise license commitment</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>Mission critical 99.99% availability SLA guarantee included</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>17.5% volume rate lock applied for full term duration</span>
          </div>
        </div>
      </div>
    </div>
  );
};
