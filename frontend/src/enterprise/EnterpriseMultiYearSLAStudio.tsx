import React, { useState } from "react";
import { ShieldCheck, Award, CheckCircle2, Clock } from "lucide-react";

export const EnterpriseMultiYearSLAStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            Mission-Critical Enterprise SLA & Service Credit Schedule
          </h3>
          <p className="text-xs text-slate-400">Multi-year contractual uptime guarantees with automated financial credit schedules</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          99.99% Guaranteed
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Sev-1 Response Time</span>
          <div className="text-2xl font-bold text-emerald-400">&lt; 15 Mins</div>
          <span className="text-[10px] text-slate-400">24x7x365 Hotline</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Dedicated TAM</span>
          <div className="text-2xl font-bold text-white">Assigned</div>
          <span className="text-[10px] text-emerald-400">Named Technical Architect</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Max Credit Offset</span>
          <div className="text-2xl font-bold text-white">50% Credit</div>
          <span className="text-[10px] text-slate-400">If Uptime Drops Below 99.0%</span>
        </div>
      </div>
    </div>
  );
};
