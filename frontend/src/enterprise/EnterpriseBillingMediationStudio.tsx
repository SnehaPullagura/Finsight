import React, { useState } from "react";
import { Zap, DollarSign, Database, CheckCircle2 } from "lucide-react";

export const EnterpriseBillingMediationStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Zap className="w-5 h-5 text-emerald-400" />
            High-Throughput Billing Mediation & Usage Rating Engine
          </h3>
          <p className="text-xs text-slate-400">Zero-latency rating of streaming usage events, allowance drawdowns, and overage calculations</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Rated Active
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">API Invocations Rated</span>
          <div className="text-2xl font-bold text-white">4.82M Calls</div>
          <span className="text-[10px] text-slate-400">Included Allowance: 5.0M</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Allowance Utilization</span>
          <div className="text-2xl font-bold text-emerald-400">96.4%</div>
          <span className="text-[10px] text-emerald-400">Optimal Consumption Pacing</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Metered Overage Incurred</span>
          <div className="text-2xl font-bold text-white">$0.00</div>
          <span className="text-[10px] text-slate-400">Within Standard Tier</span>
        </div>
      </div>
    </div>
  );
};
