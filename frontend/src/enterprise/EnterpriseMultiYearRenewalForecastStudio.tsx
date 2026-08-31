import React, { useState } from "react";
import { TrendingUp, Award, DollarSign, CheckCircle2 } from "lucide-react";

export const EnterpriseMultiYearRenewalForecastStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-emerald-400" />
            Multi-Year Enterprise Renewal Forecast Matrix
          </h3>
          <p className="text-xs text-slate-400">Weighted probability forecast of recurring revenue locked under multi-year contracts</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          96.4% Renewal Rate
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Multi-Year ARR Base</span>
          <div className="text-2xl font-bold text-white">$8.45M ARR</div>
          <span className="text-[10px] text-slate-400">64 Enterprise Accounts</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Projected Locked ARR</span>
          <div className="text-2xl font-bold text-emerald-400">$8.15M ARR</div>
          <span className="text-[10px] text-emerald-400">High Confidence Renewal</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Average Commitment</span>
          <div className="text-2xl font-bold text-white">2.8 Years</div>
          <span className="text-[10px] text-slate-400">Co-Termed Master Service Agreements</span>
        </div>
      </div>
    </div>
  );
};
