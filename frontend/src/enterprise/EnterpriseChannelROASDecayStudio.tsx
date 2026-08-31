import React, { useState } from "react";
import { TrendingDown, DollarSign, Target, CheckCircle2 } from "lucide-react";

export const EnterpriseChannelROASDecayStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Target className="w-5 h-5 text-emerald-400" />
            Channel ROAS Scaling & Decay Simulation
          </h3>
          <p className="text-xs text-slate-400">Power-law decay curve predicting return on ad spend at increased budget scale</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Simulated: 6.8x ROAS
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Simulated Spend Scale</span>
          <div className="text-2xl font-bold text-white">$150,000 / Mo</div>
          <span className="text-[10px] text-slate-400">3x Budget Expansion</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Projected Scaled ROAS</span>
          <div className="text-2xl font-bold text-emerald-400">6.8x Multiplier</div>
          <span className="text-[10px] text-slate-400">Decayed from 8.5x Baseline</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Projected Monthly Revenue</span>
          <div className="text-2xl font-bold text-white">$1,020,000</div>
          <span className="text-[10px] text-emerald-400">+$595k Net Added Revenue</span>
        </div>
      </div>
    </div>
  );
};
