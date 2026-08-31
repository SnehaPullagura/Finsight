import React, { useState } from "react";
import { Users, ShieldCheck, CheckCircle2, Award } from "lucide-react";

export const EnterpriseSponsorAlignmentStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Users className="w-5 h-5 text-emerald-400" />
            Executive Sponsor & Economic Buyer Alignment Matrix
          </h3>
          <p className="text-xs text-slate-400">Governance index ensuring every top-tier ARR account has an active VP/C-Suite sponsor</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          94.2% Sponsor Coverage
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Tier 1 Accounts Audited</span>
          <div className="text-2xl font-bold text-white">48 Accounts</div>
          <span className="text-[10px] text-slate-400">&gt; $100k ARR Cohort</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Sponsor Aligned</span>
          <div className="text-2xl font-bold text-emerald-400">45 Accounts</div>
          <span className="text-[10px] text-emerald-400">C-Level / VP Confirmed</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Sponsor Gap</span>
          <div className="text-2xl font-bold text-amber-400">3 Accounts</div>
          <span className="text-[10px] text-slate-400">CSM Outreach Assigned</span>
        </div>
      </div>
    </div>
  );
};
