import React, { useState } from "react";
import { Target, TrendingUp, DollarSign, RefreshCw, CheckCircle2 } from "lucide-react";

export const EnterpriseChannelROASOptimizerStudio: React.FC = () => {
  const allocations = [
    { channel: "Google Search (High Intent)", roas: "12.4x", budget: "$45,000", pct: "45.0%", projected: "$558,000" },
    { channel: "Executive Outbound SDR", roas: "8.6x", budget: "$35,000", pct: "35.0%", projected: "$301,000" },
    { channel: "LinkedIn Account-Based Ads", roas: "5.2x", budget: "$20,000", pct: "20.0%", projected: "$104,000" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Target className="w-5 h-5 text-emerald-400" />
            Algorithmic ROAS Marketing Budget Optimizer
          </h3>
          <p className="text-xs text-slate-400">Dynamic quadratic allocation model maximizing total enterprise pipeline return on ad spend</p>
        </div>
      </div>

      <div className="space-y-3">
        {allocations.map((a, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{a.channel}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Historical ROAS: {a.roas} • Share: {a.pct}</div>
            </div>
            <div className="text-right">
              <span className="text-sm font-bold text-emerald-400">{a.budget} Budget</span>
              <span className="text-[10px] text-slate-500 block">→ {a.projected} Projected Rev</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
