import React, { useState } from "react";
import { CheckCircle2, ShieldCheck, DollarSign, Award } from "lucide-react";

export const EnterpriseExpansionDealEvaluatorStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            Automated Expansion Deal Viability & Margin Gate
          </h3>
          <p className="text-xs text-slate-400">Instant validation of expansion discounts against customer health and multi-year contract terms</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Auto-Approved (Score 88/100)
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Customer Health Score</span>
          <div className="text-2xl font-bold text-emerald-400">92 / 100</div>
          <span className="text-[10px] text-emerald-400">Elite Champion Account</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Discount Concession</span>
          <div className="text-2xl font-bold text-white">10.0% Off List</div>
          <span className="text-[10px] text-emerald-400">Within Standard Tier Band</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Contract Commitment</span>
          <div className="text-2xl font-bold text-white">24 Months</div>
          <span className="text-[10px] text-emerald-400">Multi-Year Co-Termed MSA</span>
        </div>
      </div>
    </div>
  );
};
