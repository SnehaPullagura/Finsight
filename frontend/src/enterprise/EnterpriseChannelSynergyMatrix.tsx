import React, { useState } from "react";
import { TrendingUp, Layers, CheckCircle2, ArrowRight } from "lucide-react";

export const EnterpriseChannelSynergyMatrix: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Layers className="w-5 h-5 text-emerald-400" />
            Multi-Touch Marketing Synergy & Lift Matrix
          </h3>
          <p className="text-xs text-slate-400">Conversion velocity comparison between single-channel vs omnichannel buyer journeys</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          +14.2% Synergy Lift
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Single Touch Conversion</span>
          <div className="text-2xl font-bold text-slate-300">12.4%</div>
          <span className="text-[10px] text-slate-500">Search or Ad Only</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Omnichannel Conversion</span>
          <div className="text-2xl font-bold text-emerald-400">26.6%</div>
          <span className="text-[10px] text-emerald-400">Search + Ad + Webinar</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Net Synergy Lift</span>
          <div className="text-2xl font-bold text-purple-400">+14.2%</div>
          <span className="text-[10px] text-purple-400">2.1x Higher Close Rate</span>
        </div>
      </div>
    </div>
  );
};
