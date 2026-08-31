import React, { useState } from "react";
import { DollarSign, RefreshCw, CheckCircle2, Award } from "lucide-react";

export const EnterpriseCreditRolloverStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <DollarSign className="w-5 h-5 text-emerald-400" />
            Prepaid Commit Credit Expiration & Rollover Policy
          </h3>
          <p className="text-xs text-slate-400">Automated 20% credit rollover calculations incentivizing early enterprise contract renewals</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          20% Max Rollover
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Unused Credit Balance</span>
          <div className="text-2xl font-bold text-white">$14,500</div>
          <span className="text-[10px] text-slate-400">Year 1 Ending Prepaid Pool</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Rolled Over to Year 2</span>
          <div className="text-2xl font-bold text-emerald-400">$2,900</div>
          <span className="text-[10px] text-emerald-400">Applied to Renewal Term</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Forfeited Breakage</span>
          <div className="text-2xl font-bold text-white">$11,600</div>
          <span className="text-[10px] text-slate-400">Recognized as Contract Breakage</span>
        </div>
      </div>
    </div>
  );
};
