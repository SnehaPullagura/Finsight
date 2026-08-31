import React, { useState } from "react";
import { TrendingUp, DollarSign, Award, CheckCircle2 } from "lucide-react";

export const EnterpriseRepIRRCalculatorStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-emerald-400" />
            Sales Hiring Internal Rate of Return (IRR) Calculator
          </h3>
          <p className="text-xs text-slate-400">Discounted cash flow model and annualized IRR per newly added quota-carrying AE headcount</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          142.5% Annualized IRR
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Fully-Loaded Onboarding Cost</span>
          <div className="text-2xl font-bold text-white">$120,000</div>
          <span className="text-[10px] text-slate-400">Base, Tech Stack & Enablement</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">2-Year Gross Margin Inflow</span>
          <div className="text-2xl font-bold text-emerald-400">$462,000</div>
          <span className="text-[10px] text-emerald-400">3.85x Cash Multiple</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Net Capacity Margin</span>
          <div className="text-2xl font-bold text-emerald-400">+$342,000</div>
          <span className="text-[10px] text-slate-400">Net Contributed Value</span>
        </div>
      </div>
    </div>
  );
};
