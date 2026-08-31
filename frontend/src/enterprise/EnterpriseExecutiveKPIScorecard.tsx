import React, { useState } from "react";
import { Award, TrendingUp, CheckCircle2, DollarSign, Target, Activity } from "lucide-react";

export const EnterpriseExecutiveKPIScorecard: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Award className="w-5 h-5 text-emerald-400" />
            Executive SaaS Performance Scorecard & Rule of 40
          </h3>
          <p className="text-xs text-slate-400">Board-level financial and operational efficiency metrics</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Top Decile SaaS
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Rule of 40 Index</span>
          <div className="text-2xl font-bold text-emerald-400">54.2%</div>
          <span className="text-[10px] text-slate-400">38.2% Growth + 16.0% FCF</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">SaaS Magic Number</span>
          <div className="text-2xl font-bold text-white">1.34x</div>
          <span className="text-[10px] text-emerald-400">High S&M Capital Efficiency</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">LTV : CAC Ratio</span>
          <div className="text-2xl font-bold text-white">4.8x</div>
          <span className="text-[10px] text-emerald-400">Industry Target: 3.0x+</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">CAC Payback Period</span>
          <div className="text-2xl font-bold text-white">9.2 Months</div>
          <span className="text-[10px] text-emerald-400">Top-Quartile Recovery</span>
        </div>
      </div>
    </div>
  );
};
