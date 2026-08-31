import React, { useState } from "react";
import { Activity, Users, Zap, TrendingUp, CheckCircle2 } from "lucide-react";

export const EnterpriseProductUsageTelemetry: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Activity className="w-5 h-5 text-emerald-400" />
            Product Usage Telemetry & DAU / MAU Stickiness
          </h3>
          <p className="text-xs text-slate-400">User session velocity, active feature adoption, and engagement stickiness</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Top Tier Stickiness (42.5%)
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Daily Active Users (DAU)</span>
          <div className="text-2xl font-bold text-white">4,250</div>
          <span className="text-[10px] text-emerald-400">↑ 18.2% MoM</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Monthly Active Users (MAU)</span>
          <div className="text-2xl font-bold text-white">10,000</div>
          <span className="text-[10px] text-emerald-400">↑ 12.0% MoM</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">DAU / MAU Ratio</span>
          <div className="text-2xl font-bold text-emerald-400">42.5%</div>
          <span className="text-[10px] text-slate-400">Benchmark: 20%+</span>
        </div>
      </div>
    </div>
  );
};
