import React, { useState } from "react";
import { Zap, Target, TrendingUp, CheckCircle2 } from "lucide-react";

export const EnterprisePipelineVelocityAttributionStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Zap className="w-5 h-5 text-emerald-400" />
            Marketing Creative Pipeline Velocity Attribution
          </h3>
          <p className="text-xs text-slate-400">Multi-touch W-shaped attribution mapping interactive collateral directly to closed revenue</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          +$6.8M Influenced
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Top Converting Creative</span>
          <div className="text-2xl font-bold text-white">Interactive CPQ Tour</div>
          <span className="text-[10px] text-emerald-400">42.5% Pipeline Influence Share</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Attributed Closed ARR</span>
          <div className="text-2xl font-bold text-emerald-400">$2,890,000</div>
          <span className="text-[10px] text-slate-400">18 Enterprise Closed-Won Deals</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Attribution Model</span>
          <div className="text-2xl font-bold text-white">W-Shaped 40/40/20</div>
          <span className="text-[10px] text-slate-400">First / Mid / Opportunity Touch</span>
        </div>
      </div>
    </div>
  );
};
