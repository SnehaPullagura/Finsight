import React, { useState } from "react";
import { Award, TrendingUp, DollarSign, CheckCircle2 } from "lucide-react";

export const EnterpriseRepRetentionScoringStudio: React.FC = () => {
  const reps = [
    { name: "Alex Vance", baseline: "$540,000", retained: "$620,000", nrr: "114.8%", tier: "World Class" },
    { name: "Sarah Connor", baseline: "$680,000", retained: "$710,000", nrr: "104.4%", tier: "Solid Retention" },
    { name: "John Wick", baseline: "$320,000", retained: "$295,000", nrr: "92.2%", tier: "Elevated Churn" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Award className="w-5 h-5 text-emerald-400" />
            Sales Rep Customer Retention & NRR Cohort Scoring
          </h3>
          <p className="text-xs text-slate-400">12-month cohort Net Revenue Retention (NRR) achieved on closed accounts by sales rep</p>
        </div>
      </div>

      <div className="space-y-3">
        {reps.map((r, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{r.name}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Closed: {r.baseline} → 12M Retained: {r.retained}</div>
            </div>
            <div className="text-right">
              <span className="text-sm font-bold text-emerald-400">{r.nrr} NRR</span>
              <span className="text-[10px] text-slate-500 block">{r.tier}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
