import React, { useState } from "react";
import { Clock, Zap, CheckCircle2, TrendingUp } from "lucide-react";

export const EnterpriseMQLAgingVelocityStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Zap className="w-5 h-5 text-emerald-400" />
            MQL Inbound Speed-to-Lead Velocity
          </h3>
          <p className="text-xs text-slate-400">Distribution of inbound lead outreach response times across SDR team</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          92.4% Under 24 Hours
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">&lt; 24 Hours (Fast Track)</span>
          <div className="text-xl font-bold text-emerald-400">450 Leads</div>
          <span className="text-[10px] text-emerald-400">92.4% of Total Inbound</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">1 - 3 Days</span>
          <div className="text-xl font-bold text-white">28 Leads</div>
          <span className="text-[10px] text-slate-400">5.7% of Inbound</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">3 - 7 Days</span>
          <div className="text-xl font-bold text-white">7 Leads</div>
          <span className="text-[10px] text-slate-400">1.4% of Inbound</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">&gt; 7 Days (Stale)</span>
          <div className="text-xl font-bold text-slate-500">2 Leads</div>
          <span className="text-[10px] text-slate-500">0.5%</span>
        </div>
      </div>
    </div>
  );
};
