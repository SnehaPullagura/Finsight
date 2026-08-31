import React, { useState } from "react";
import { DollarSign, ShieldCheck, CheckCircle2, Award } from "lucide-react";

export const EnterpriseMultiYearDiscountStudio: React.FC = () => {
  const tiers = [
    { term: "1 Year Standard", disc: "0.0%", annual: "$100,000", tcv: "$100,000", savings: "$0" },
    { term: "2 Year Strategic", disc: "10.0%", annual: "$90,000", tcv: "$180,000", savings: "$20,000" },
    { term: "3 Year Enterprise", disc: "17.5%", annual: "$82,500", tcv: "$247,500", savings: "$52,500" },
    { term: "5 Year Transformational", disc: "25.0%", annual: "$75,000", tcv: "$375,000", savings: "$125,000" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <DollarSign className="w-5 h-5 text-emerald-400" />
            Multi-Year Commitment Discount & TCV Optimizer
          </h3>
          <p className="text-xs text-slate-400">Standardized multi-year discount schedules maximizing Total Contract Value (TCV) retention</p>
        </div>
      </div>

      <div className="space-y-3">
        {tiers.map((t, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{t.term}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Discount: {t.disc} • Annualized: {t.annual} • Total Savings: <span className="text-emerald-400 font-bold">{t.savings}</span></div>
            </div>
            <div className="text-right">
              <span className="text-sm font-bold text-emerald-400">{t.tcv} TCV</span>
              <span className="text-[10px] text-slate-500 block">Pre-Approved CPQ Guard</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
