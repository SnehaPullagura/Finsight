import React, { useState } from "react";
import { TrendingUp, DollarSign, Layers, CheckCircle2 } from "lucide-react";

export const EnterpriseBoardRevenueWaterfall: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-emerald-400" />
            Board of Directors ARR Revenue Waterfall Bridge
          </h3>
          <p className="text-xs text-slate-400">Quarterly ARR bridge decomposing new logo acquisition, expansion, and logo churn</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          +$3.25M Net ARR Growth
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Starting ARR</span>
          <div className="text-2xl font-bold text-white">$12.5M</div>
          <span className="text-[10px] text-slate-400">Q1 Baseline</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Gross New Added</span>
          <div className="text-2xl font-bold text-emerald-400">+$3.85M</div>
          <span className="text-[10px] text-emerald-400">New Logo + Upsell</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Total Lost ARR</span>
          <div className="text-2xl font-bold text-red-400">-$600K</div>
          <span className="text-[10px] text-red-400">4.8% Logo Churn</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Ending ARR</span>
          <div className="text-2xl font-bold text-white">$15.75M</div>
          <span className="text-[10px] text-emerald-400">+26.0% QoQ Expansion</span>
        </div>
      </div>
    </div>
  );
};
