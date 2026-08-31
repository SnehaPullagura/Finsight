import React, { useState } from "react";
import { Smile, TrendingUp, CheckCircle2, Award } from "lucide-react";

export const EnterpriseCSATTrendsDashboard: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Smile className="w-5 h-5 text-emerald-400" />
            Customer Satisfaction (CSAT) Trajectory Dashboard
          </h3>
          <p className="text-xs text-slate-400">Quarterly post-support ticket CSAT rating distribution and trend momentum</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          96.4% CSAT (Top Decile)
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Overall CSAT</span>
          <div className="text-2xl font-bold text-emerald-400">96.4%</div>
          <span className="text-[10px] text-slate-400">↑ +2.1% MoM Improvement</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">First Contact Resolution</span>
          <div className="text-2xl font-bold text-white">88.5%</div>
          <span className="text-[10px] text-emerald-400">Target: 80%+</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Avg Resolution Time</span>
          <div className="text-2xl font-bold text-white">2.4 Hours</div>
          <span className="text-[10px] text-emerald-400">100% SLA Compliant</span>
        </div>
      </div>
    </div>
  );
};
