import React, { useState } from "react";
import { Flame, Target, TrendingDown, CheckCircle2 } from "lucide-react";

export const EnterpriseCreativeFatigueIndexStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Flame className="w-5 h-5 text-amber-400" />
            Ad Creative Fatigue Index & Burnout Diagnostics
          </h3>
          <p className="text-xs text-slate-400">Algorithmic fatigue score tracking audience frequency saturation and CPM inflation</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Score: 32.4 / 100 (Fresh)
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Average Frequency</span>
          <div className="text-2xl font-bold text-white">2.4x / User</div>
          <span className="text-[10px] text-emerald-400">Safe Frequency Band</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">CTR Degradation</span>
          <div className="text-2xl font-bold text-emerald-400">-4.2% MoM</div>
          <span className="text-[10px] text-slate-400">Normal Audience Variance</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">CPM Inflation</span>
          <div className="text-2xl font-bold text-white">+$1.20 CPM</div>
          <span className="text-[10px] text-emerald-400">Stable Bidding Dynamics</span>
        </div>
      </div>
    </div>
  );
};
