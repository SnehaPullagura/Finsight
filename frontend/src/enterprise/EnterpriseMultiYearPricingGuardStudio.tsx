import React, { useState } from "react";
import { ShieldCheck, DollarSign, CheckCircle2, AlertTriangle } from "lucide-react";

export const EnterpriseMultiYearPricingGuardStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            CPQ Multi-Year Pricing & Floor Guardrail Engine
          </h3>
          <p className="text-xs text-slate-400">Automated gross-margin protection enforcing floor pricing rules by contract duration</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Guardrail Active
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">1-Year Max Discount</span>
          <div className="text-2xl font-bold text-white">5.0% Floor</div>
          <span className="text-[10px] text-slate-400">Strict Non-Standard Escalation</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">3-Year Max Discount</span>
          <div className="text-2xl font-bold text-emerald-400">20.0% Floor</div>
          <span className="text-[10px] text-emerald-400">Pre-Approved for ACV &gt; $100k</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">5-Year Max Discount</span>
          <div className="text-2xl font-bold text-emerald-400">30.0% Floor</div>
          <span className="text-[10px] text-emerald-400">Transformational Enterprise Tier</span>
        </div>
      </div>
    </div>
  );
};
