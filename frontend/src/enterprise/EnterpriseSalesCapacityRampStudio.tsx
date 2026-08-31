import React, { useState } from "react";
import { Users, TrendingUp, DollarSign, CheckCircle2 } from "lucide-react";

export const EnterpriseSalesCapacityRampStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Users className="w-5 h-5 text-emerald-400" />
            AE Sales Quota Capacity & Ramp Pacing Simulator
          </h3>
          <p className="text-xs text-slate-400">Tenure-adjusted effective capacity model forecasting total annualized sales runway</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          14.25 Effective AEs
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Total AE Headcount</span>
          <div className="text-2xl font-bold text-white">18 Sales Reps</div>
          <span className="text-[10px] text-slate-400">12 Fully Ramped / 6 Onboarding</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Ramped Capacity Factor</span>
          <div className="text-2xl font-bold text-emerald-400">79.2%</div>
          <span className="text-[10px] text-emerald-400">Effective Productivity</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Annualized Capacity</span>
          <div className="text-2xl font-bold text-white">$14.25M Quota</div>
          <span className="text-[10px] text-slate-400">$1M Quota / Fully Ramped AE</span>
        </div>
      </div>
    </div>
  );
};
