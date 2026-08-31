import React, { useState } from "react";
import { TrendingUp, RefreshCw, CheckCircle2, DollarSign } from "lucide-react";

export const EnterprisePipelineDriftStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-emerald-400" />
            Quarterly Pipeline Drift & Net Velocity Heatmap
          </h3>
          <p className="text-xs text-slate-400">Week-over-week bridge tracking new pipeline added, closed-won ARR, and slipped deals</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          +$680k Net Weekly Drift
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">New Sourced Pipeline</span>
          <div className="text-2xl font-bold text-emerald-400">+$950,000</div>
          <span className="text-[10px] text-slate-400">14 New Qualified Opportunities</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Closed-Won Inflow</span>
          <div className="text-2xl font-bold text-emerald-400">+$420,000</div>
          <span className="text-[10px] text-emerald-400">3 Enterprise Deals Converted</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Slipped to Next Quarter</span>
          <div className="text-2xl font-bold text-amber-400">-$690,000</div>
          <span className="text-[10px] text-slate-400">2 Deals in Legal Extended Review</span>
        </div>
      </div>
    </div>
  );
};
