import React, { useState } from "react";
import { AlertCircle, Clock, CheckCircle2, TrendingDown } from "lucide-react";

export const EnterpriseDealSlippageMatrix: React.FC = () => {
  const atRiskDeals = [
    { name: "Wayne Enterprises Global MSA", value: "$250,000", pushCount: 3, daysStagnant: 28, risk: "Critical" },
    { name: "Oscorp Enterprise AI Rollout", value: "$180,000", pushCount: 2, daysStagnant: 18, risk: "Elevated" },
    { name: "Cyberdyne Systems Security Suite", value: "$95,000", pushCount: 1, daysStagnant: 12, risk: "Moderate" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <TrendingDown className="w-5 h-5 text-amber-400" />
            Deal Slippage Early Warning System
          </h3>
          <p className="text-xs text-slate-400">Identify deals with multiple close date delays and stage stagnation</p>
        </div>
      </div>

      <div className="space-y-3">
        {atRiskDeals.map((deal, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{deal.name}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">
                {deal.value} • Pushed {deal.pushCount} times • {deal.daysStagnant} days in stage
              </div>
            </div>
            <span className={`text-xs font-bold px-2.5 py-1 rounded-full ${
              deal.risk === "Critical" ? "bg-red-950 text-red-400 border border-red-800" :
              deal.risk === "Elevated" ? "bg-amber-950 text-amber-400 border border-amber-800" : "bg-blue-950 text-blue-400 border border-blue-800"
            }`}>
              {deal.risk}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
