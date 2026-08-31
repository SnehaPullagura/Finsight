import React, { useState } from "react";
import { TrendingUp, Users, DollarSign, Award, CheckCircle2 } from "lucide-react";

export const EnterpriseExpansionPropensityStudio: React.FC = () => {
  const accounts = [
    { name: "Wayne Enterprises", score: 94, arr: "$250,000", play: "Advanced Security Addon", tier: "High Propensity" },
    { name: "Stark Industries", score: 89, arr: "$180,000", play: "Additional 50 Seats", tier: "High Propensity" },
    { name: "Oscorp Holdings", score: 72, arr: "$95,000", play: "AI Copilot Module", tier: "Moderate" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-emerald-400" />
            Account Upsell & Expansion Propensity Matrix
          </h3>
          <p className="text-xs text-slate-400">Multi-variate algorithmic readiness scoring for seat and feature expansion</p>
        </div>
      </div>

      <div className="space-y-3">
        {accounts.map((a, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{a.name}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Base ARR: {a.arr} • Recommended: {a.play}</div>
            </div>
            <div className="text-right">
              <span className="text-sm font-bold text-emerald-400">{a.score} / 100</span>
              <span className="text-[10px] text-slate-500 block">{a.tier}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
