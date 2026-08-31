import React, { useState } from "react";
import { Calculator, DollarSign, TrendingUp, CheckCircle2 } from "lucide-react";

export const EnterpriseLTVModelerStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Calculator className="w-5 h-5 text-emerald-400" />
            Customer Lifetime Value (LTV) Actuarial Modeler
          </h3>
          <p className="text-xs text-slate-400">Discounted cash flow (DCF) actuarial LTV projections based on empirical cohort churn</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Discounted LTV</span>
          <div className="text-2xl font-bold text-emerald-400">$184,500</div>
          <span className="text-[10px] text-slate-400">8.0% Annual Discount Rate</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Average Lifespan</span>
          <div className="text-2xl font-bold text-white">41.6 Months</div>
          <span className="text-[10px] text-emerald-400">0.8% Monthly Logo Churn</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Gross Margin</span>
          <div className="text-2xl font-bold text-white">82.5%</div>
          <span className="text-[10px] text-slate-400">SaaS Cloud Infrastructure Model</span>
        </div>
      </div>
    </div>
  );
};
