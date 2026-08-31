import React, { useState } from "react";
import { TrendingUp, Award, CheckCircle2, Shuffle } from "lucide-react";

export const EnterpriseMonteCarloPipelineStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Shuffle className="w-5 h-5 text-emerald-400" />
            10,000-Iteration Monte Carlo Revenue Simulator
          </h3>
          <p className="text-xs text-slate-400">Statistical pipeline probability modeling providing P10, P50, and P90 quarterly landing bands</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          P50: $3.85M ARR
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Conservative Band (P10)</span>
          <div className="text-2xl font-bold text-white">$3.20M ARR</div>
          <span className="text-[10px] text-slate-400">90% Statistical Confidence</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Most Likely Band (P50)</span>
          <div className="text-2xl font-bold text-emerald-400">$3.85M ARR</div>
          <span className="text-[10px] text-emerald-400">Expected Quarter Landing</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Upside Band (P90)</span>
          <div className="text-2xl font-bold text-white">$4.45M ARR</div>
          <span className="text-[10px] text-slate-400">Accelerated Close Scenarios</span>
        </div>
      </div>
    </div>
  );
};
