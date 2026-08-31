import React, { useState } from "react";
import { Calculator, TrendingUp, DollarSign, CheckCircle2 } from "lucide-react";

export const EnterpriseCACPaybackSensitivityStudio: React.FC = () => {
  const sensitivities = [
    { churn: "0.5% / Mo", payback: "7.2 Mo", ltv: "$240,000", ratio: "8.2x", health: "Exceptional" },
    { churn: "1.0% / Mo", payback: "7.2 Mo", ltv: "$120,000", ratio: "4.1x", health: "Healthy" },
    { churn: "2.0% / Mo", payback: "7.2 Mo", ltv: "$60,000", ratio: "2.1x", health: "Vulnerable" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Calculator className="w-5 h-5 text-emerald-400" />
            CAC Payback & Churn Sensitivity Matrix
          </h3>
          <p className="text-xs text-slate-400">Stress-testing unit economics and LTV:CAC multiples under fluctuating churn rate scenarios</p>
        </div>
      </div>

      <div className="space-y-3">
        {sensitivities.map((s, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">Scenario: {s.churn} Churn</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Payback: {s.payback} • Implied LTV: {s.ltv}</div>
            </div>
            <div className="text-right">
              <span className="text-sm font-bold text-emerald-400">{s.ratio} LTV:CAC</span>
              <span className="text-[10px] text-slate-500 block">{s.health}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
