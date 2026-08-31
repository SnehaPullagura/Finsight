import React, { useState } from "react";
import { TrendingUp, Award, DollarSign, CheckCircle2 } from "lucide-react";

export const EnterpriseCohortGrossRetentionStudio: React.FC = () => {
  const cohorts = [
    { qtr: "Q1 2025 Cohort", base: "$2.4M", grr: "96.2%", nrr: "118.4%", status: "Elite Top Quartile" },
    { qtr: "Q2 2025 Cohort", base: "$3.1M", grr: "95.8%", nrr: "116.2%", status: "Elite Top Quartile" },
    { qtr: "Q3 2025 Cohort", base: "$3.8M", grr: "94.5%", nrr: "114.8%", status: "Healthy" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-emerald-400" />
            Cohort Gross Revenue (GRR) & Net Revenue Retention (NRR)
          </h3>
          <p className="text-xs text-slate-400">Quarterly onboarding cohort retention matrix isolating organic expansion from customer churn</p>
        </div>
      </div>

      <div className="space-y-3">
        {cohorts.map((c, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{c.qtr}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Base ARR: {c.base} • GRR: <span className="text-emerald-400 font-bold">{c.grr}</span> • NRR: <span className="text-emerald-400 font-bold">{c.nrr}</span></div>
            </div>
            <span className="text-xs font-semibold bg-emerald-950 text-emerald-400 border border-emerald-800 px-2.5 py-1 rounded-full">
              {c.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
