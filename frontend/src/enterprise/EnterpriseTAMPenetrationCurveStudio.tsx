import React, { useState } from "react";
import { Globe, TrendingUp, PieChart, CheckCircle2 } from "lucide-react";

export const EnterpriseTAMPenetrationCurveStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Globe className="w-5 h-5 text-emerald-400" />
            Market TAM Penetration & White-Space Radar
          </h3>
          <p className="text-xs text-slate-400">Total addressable market account penetration vs actively engaged pipeline accounts</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          7.2% Penetration (Challenger)
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Acquired Customer Accounts</span>
          <div className="text-2xl font-bold text-emerald-400">864 Accounts</div>
          <span className="text-[10px] text-slate-400">7.2% of Total 12,000 Target TAM</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Active Pipeline Engaged</span>
          <div className="text-2xl font-bold text-white">1,420 Accounts</div>
          <span className="text-[10px] text-emerald-400">11.8% of Total TAM in Motion</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Unreached White Space</span>
          <div className="text-2xl font-bold text-slate-400">9,716 Accounts</div>
          <span className="text-[10px] text-slate-400">81.0% Expansion Opportunity</span>
        </div>
      </div>
    </div>
  );
};
