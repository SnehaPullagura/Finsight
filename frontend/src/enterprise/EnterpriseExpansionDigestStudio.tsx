import React, { useState } from "react";
import { Mail, TrendingUp, CheckCircle2, DollarSign } from "lucide-react";

export const EnterpriseExpansionDigestStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Mail className="w-5 h-5 text-emerald-400" />
            Weekly CS Expansion & Upsell Intelligence Digest
          </h3>
          <p className="text-xs text-slate-400">Executive email summary of qualified high-health expansion opportunities</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Digest Active
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Expansion Opportunities</span>
          <div className="text-2xl font-bold text-white">14 Accounts</div>
          <span className="text-[10px] text-slate-400">Health 85+ with 90%+ Seat Usage</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Total Potential Pipeline</span>
          <div className="text-2xl font-bold text-emerald-400">$640,000 ARR</div>
          <span className="text-[10px] text-emerald-400">+$45k Average Upsell ACV</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Auto-Sync Cadence</span>
          <div className="text-2xl font-bold text-white">Every Monday</div>
          <span className="text-[10px] text-slate-400">Slack #sales-leads & Email</span>
        </div>
      </div>
    </div>
  );
};
