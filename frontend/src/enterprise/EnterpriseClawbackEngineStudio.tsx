import React, { useState } from "react";
import { AlertCircle, DollarSign, ShieldCheck, CheckCircle2 } from "lucide-react";

export const EnterpriseClawbackEngineStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            Commission Clawback & Retention Governance Engine
          </h3>
          <p className="text-xs text-slate-400">Automated clawback calculation rules for early customer contract terminations</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Policy Active
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">0 - 90 Days Churn</span>
          <div className="text-2xl font-bold text-red-400">100% Clawback</div>
          <span className="text-[10px] text-slate-400">Full Unvested Commission Recovery</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">91 - 180 Days Churn</span>
          <div className="text-2xl font-bold text-amber-400">50% Clawback</div>
          <span className="text-[10px] text-slate-400">Partial Shared-Risk Offset</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">181+ Days Active</span>
          <div className="text-2xl font-bold text-emerald-400">0% Clawback</div>
          <span className="text-[10px] text-emerald-400">Fully Vested Commission</span>
        </div>
      </div>
    </div>
  );
};
