import React, { useState } from "react";
import { DollarSign, Flame, TrendingUp, CheckCircle2 } from "lucide-react";

export const EnterpriseBurnMultipleStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Flame className="w-5 h-5 text-amber-400" />
            Capital Efficiency & Burn Multiple Modeler
          </h3>
          <p className="text-xs text-slate-400">Net cash burn per dollar of net new ARR generated</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          0.82x (Top Decile SaaS)
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Net Cash Burned</span>
          <div className="text-2xl font-bold text-white">$1,640,000</div>
          <span className="text-[10px] text-slate-400">Annualized Run Rate</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Net New ARR Generated</span>
          <div className="text-2xl font-bold text-emerald-400">$2,000,000</div>
          <span className="text-[10px] text-emerald-400">+100% ARR Growth</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Burn Multiple</span>
          <div className="text-2xl font-bold text-emerald-400">0.82x</div>
          <span className="text-[10px] text-slate-400">$0.82 Burned per $1.00 ARR</span>
        </div>
      </div>
    </div>
  );
};
