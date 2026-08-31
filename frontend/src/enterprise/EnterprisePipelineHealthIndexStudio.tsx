import React, { useState } from "react";
import { Activity, ShieldCheck, TrendingUp, CheckCircle2 } from "lucide-react";

export const EnterprisePipelineHealthIndexStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Activity className="w-5 h-5 text-emerald-400" />
            Executive Pipeline Health Index (PHI)
          </h3>
          <p className="text-xs text-slate-400">Composite algorithmic index tracking pipeline coverage, deal freshness, and slippage stability</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Score: 88.4 / 100 (Elite)
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Coverage Component</span>
          <div className="text-2xl font-bold text-emerald-400">48.2 / 50</div>
          <span className="text-[10px] text-slate-400">3.4x Quota Coverage Multiple</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Freshness Component</span>
          <div className="text-2xl font-bold text-white">21.8 / 25</div>
          <span className="text-[10px] text-emerald-400">22.4 Days Average Age</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Stability Component</span>
          <div className="text-2xl font-bold text-white">18.4 / 25</div>
          <span className="text-[10px] text-slate-400">&lt; 12% Quarterly Push Rate</span>
        </div>
      </div>
    </div>
  );
};
