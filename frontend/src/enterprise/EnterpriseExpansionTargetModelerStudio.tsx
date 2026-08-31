import React, { useState } from "react";
import { Target, TrendingUp, DollarSign, Award, CheckCircle2 } from "lucide-react";

export const EnterpriseExpansionTargetModelerStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Target className="w-5 h-5 text-emerald-400" />
            Portfolio ARR Expansion Runway & Target Modeler
          </h3>
          <p className="text-xs text-slate-400">Simulate 12-month net expansion runway across installed enterprise account cohorts</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          +25.0% Expansion Target
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Installed Base Baseline</span>
          <div className="text-2xl font-bold text-white">$14.2M ARR</div>
          <span className="text-[10px] text-slate-400">128 Enterprise Accounts</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Target Expansion Net</span>
          <div className="text-2xl font-bold text-emerald-400">+$3.55M ARR</div>
          <span className="text-[10px] text-emerald-400">Seat Upsell & Advanced Modules</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Projected Ending ARR</span>
          <div className="text-2xl font-bold text-white">$17.75M ARR</div>
          <span className="text-[10px] text-emerald-400">125% Net Expansion Pace</span>
        </div>
      </div>
    </div>
  );
};
