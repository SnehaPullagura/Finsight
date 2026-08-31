import React, { useState } from "react";
import { Target, TrendingUp, DollarSign, CheckCircle2 } from "lucide-react";

export const EnterpriseChannelElasticityStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Target className="w-5 h-5 text-emerald-400" />
            Marketing Spend Elasticity & Channel Responsiveness
          </h3>
          <p className="text-xs text-slate-400">Elasticity coefficient quantifying lead volume expansion relative to budget increases</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          1.24x Elastic (High Growth)
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Tested Budget Lift</span>
          <div className="text-2xl font-bold text-white">+25.0%</div>
          <span className="text-[10px] text-slate-400">Quarterly Channel Test</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Lead Volume Expansion</span>
          <div className="text-2xl font-bold text-emerald-400">+31.0%</div>
          <span className="text-[10px] text-emerald-400">Above Linear Growth</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Elasticity Coefficient</span>
          <div className="text-2xl font-bold text-emerald-400">1.24x</div>
          <span className="text-[10px] text-slate-400">Recommend Budget Expansion</span>
        </div>
      </div>
    </div>
  );
};
