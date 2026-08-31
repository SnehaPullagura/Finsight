import React, { useState } from "react";
import { Package, ShieldCheck, DollarSign, CheckCircle2 } from "lucide-react";

export const EnterpriseDealDeskStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Package className="w-5 h-5 text-emerald-400" />
            Executive Deal Desk & Enterprise Bundle Configurator
          </h3>
          <p className="text-xs text-slate-400">Pre-approved enterprise licensing packages with TAM and 24x7 mission-critical SLA add-ons</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          82.5% Gross Margin
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Core Platform</span>
          <div className="text-2xl font-bold text-white">$120,000</div>
          <span className="text-[10px] text-slate-400">100 Enterprise Seats</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Dedicated TAM</span>
          <div className="text-2xl font-bold text-white">$35,000</div>
          <span className="text-[10px] text-emerald-400">Named Lead Architect</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Premium SLA</span>
          <div className="text-2xl font-bold text-white">$18,000</div>
          <span className="text-[10px] text-slate-400">15-Min Response Guarantee</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Total ACV</span>
          <div className="text-2xl font-bold text-emerald-400">$173,000</div>
          <span className="text-[10px] text-emerald-400">Pre-Approved Bundle</span>
        </div>
      </div>
    </div>
  );
};
