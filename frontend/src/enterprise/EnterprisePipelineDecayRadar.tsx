import React, { useState } from "react";
import { AlertTriangle, Clock, TrendingDown, CheckCircle2 } from "lucide-react";

export const EnterprisePipelineDecayRadar: React.FC = () => {
  const decayedDeals = [
    { name: "Oscorp Systems Infrastructure", initialProb: "80%", decayedProb: "38%", daysQuiet: 45, impact: "-$54,600" },
    { name: "Cyberdyne Security License", initialProb: "60%", decayedProb: "35%", daysQuiet: 32, impact: "-$23,750" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <TrendingDown className="w-5 h-5 text-amber-400" />
            Pipeline Probability Decay & Inactivity Radar
          </h3>
          <p className="text-xs text-slate-400">Exponential probability decay modeling based on days without customer touchpoints</p>
        </div>
      </div>

      <div className="space-y-3">
        {decayedDeals.map((d, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{d.name}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">
                Initial: {d.initialProb} → Decayed: <span className="text-amber-400 font-bold">{d.decayedProb}</span> ({d.daysQuiet} days quiet)
              </div>
            </div>
            <div className="text-right">
              <span className="text-[10px] text-slate-500 uppercase font-semibold">Weighted Pipeline Loss</span>
              <div className="text-xs font-bold text-red-400">{d.impact}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
