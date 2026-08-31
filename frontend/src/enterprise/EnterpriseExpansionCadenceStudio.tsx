import React, { useState } from "react";
import { Calendar, TrendingUp, CheckCircle2, Award } from "lucide-react";

export const EnterpriseExpansionCadenceStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Calendar className="w-5 h-5 text-emerald-400" />
            Strategic Customer Expansion Outreach Cadence
          </h3>
          <p className="text-xs text-slate-400">Multi-touch communication sequence designed for expansion sales cycles</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Cadence Active
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Touchpoint 1 (Day 1)</span>
          <div className="text-xs font-bold text-white">CSM Usage Summary</div>
          <span className="text-[10px] text-slate-400">Executive ROI Metrics Email</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Touchpoint 2 (Day 4)</span>
          <div className="text-xs font-bold text-white">Roadmap Preview</div>
          <span className="text-[10px] text-slate-400">Exclusive VIP Feature Sneak Peek</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Touchpoint 3 (Day 8)</span>
          <div className="text-xs font-bold text-white">Co-Termed Quote</div>
          <span className="text-[10px] text-emerald-400">10% Volume Discount Proposal</span>
        </div>
      </div>
    </div>
  );
};
