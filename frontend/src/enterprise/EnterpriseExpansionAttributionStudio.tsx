import React, { useState } from "react";
import { TrendingUp, Layers, CheckCircle2, Award } from "lucide-react";

export const EnterpriseExpansionAttributionStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Layers className="w-5 h-5 text-emerald-400" />
            Expansion Revenue Attribution & Sourcing Matrix
          </h3>
          <p className="text-xs text-slate-400">Deconstruct expansion ARR sourced by Customer Success signals vs Product-Led growth</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          +$2.85M Expansion ARR
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">CS Health Assisted</span>
          <div className="text-2xl font-bold text-emerald-400">$1,650,000</div>
          <span className="text-[10px] text-slate-400">57.9% of Total Expansion</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Product-Led Add-Ons</span>
          <div className="text-2xl font-bold text-white">$820,000</div>
          <span className="text-[10px] text-emerald-400">28.8% Self-Service Upsell</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Sales Outbound Upsell</span>
          <div className="text-2xl font-bold text-white">$380,000</div>
          <span className="text-[10px] text-slate-400">13.3% Strategic Renewals</span>
        </div>
      </div>
    </div>
  );
};
