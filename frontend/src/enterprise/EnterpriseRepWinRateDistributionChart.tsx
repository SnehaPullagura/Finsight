import React, { useState } from "react";
import { Award, Users, TrendingUp, CheckCircle2 } from "lucide-react";

export const EnterpriseRepWinRateDistributionChart: React.FC = () => {
  const distribution = [
    { tier: "Top Performers (35%+ Win Rate)", count: 4, pct: "33.3%", color: "text-emerald-400", bg: "bg-emerald-950/30 border-emerald-800" },
    { tier: "Core Performers (20% - 35%)", count: 6, pct: "50.0%", color: "text-blue-400", bg: "bg-blue-950/30 border-blue-800" },
    { tier: "Needs Coaching (< 20%)", count: 2, pct: "16.7%", color: "text-amber-400", bg: "bg-amber-950/30 border-amber-800" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Award className="w-5 h-5 text-emerald-400" />
            Sales Rep Win Rate Cohort Distribution
          </h3>
          <p className="text-xs text-slate-400">Team performance bell-curve and opportunity conversion consistency</p>
        </div>
        <span className="text-xs text-emerald-400 font-bold bg-emerald-950 border border-emerald-800 px-3 py-1 rounded-full">
          28.4% Team Average
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {distribution.map((d, idx) => (
          <div key={idx} className={`p-4 rounded-xl border ${d.bg} space-y-1`}>
            <span className="text-[11px] text-slate-400 font-semibold">{d.tier}</span>
            <div className={`text-2xl font-bold ${d.color}`}>{d.count} Reps</div>
            <span className="text-[10px] text-slate-500">{d.pct} of Sales Organization</span>
          </div>
        ))}
      </div>
    </div>
  );
};
