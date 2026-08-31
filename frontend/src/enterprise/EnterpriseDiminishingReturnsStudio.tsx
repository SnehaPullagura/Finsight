import React, { useState } from "react";
import { TrendingDown, DollarSign, Target, CheckCircle2 } from "lucide-react";

export const EnterpriseDiminishingReturnsStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Target className="w-5 h-5 text-emerald-400" />
            Ad Spend Diminishing Returns & Marginal CAC Saturation
          </h3>
          <p className="text-xs text-slate-400">Logarithmic channel saturation curve identifying marginal acquisition cost inflation</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Healthy Scale Band
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Current Blended CAC</span>
          <div className="text-2xl font-bold text-white">$2,450</div>
          <span className="text-[10px] text-slate-400">At $50k / Mo Spend</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Marginal Incremental CAC</span>
          <div className="text-2xl font-bold text-emerald-400">$2,980</div>
          <span className="text-[10px] text-emerald-400">+$20k Incremental Budget</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">CAC Inflation</span>
          <div className="text-2xl font-bold text-white">+21.6%</div>
          <span className="text-[10px] text-emerald-400">Optimal Scale Frontier</span>
        </div>
      </div>
    </div>
  );
};
