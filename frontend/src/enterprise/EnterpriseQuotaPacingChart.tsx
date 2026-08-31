import React, { useState } from "react";
import { Target, TrendingUp, CheckCircle2 } from "lucide-react";

export const EnterpriseQuotaPacingChart: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Target className="w-5 h-5 text-emerald-400" />
            Quarterly Sales Attainment & Pacing Trajectory
          </h3>
          <p className="text-xs text-slate-400">Real-time pacing against expected linear quarter progress</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          118.5% Ahead of Plan
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Closed Revenue</span>
          <div className="text-2xl font-bold text-emerald-400">$1,850,000</div>
          <span className="text-[10px] text-slate-400">Target: $2,500,000</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Pacing Expected</span>
          <div className="text-2xl font-bold text-slate-300">62.0%</div>
          <span className="text-[10px] text-slate-500">Day 56 of 90</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Projected Finish</span>
          <div className="text-2xl font-bold text-white">$2,975,000</div>
          <span className="text-[10px] text-emerald-400">+19.0% Quota Overachievement</span>
        </div>
      </div>
    </div>
  );
};
