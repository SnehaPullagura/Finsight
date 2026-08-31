import React, { useState } from "react";
import { TrendingUp, DollarSign, Target, Award, ArrowUpRight } from "lucide-react";

export const EnterpriseMarketingEfficiencyStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Target className="w-5 h-5 text-emerald-400" />
            Marketing Capital Efficiency & ROAS Matrix
          </h3>
          <p className="text-xs text-slate-400">Blended vs Paid Customer Acquisition Cost (CAC) and campaign revenue payback</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Blended CAC</span>
          <div className="text-2xl font-bold text-emerald-400">$3,420</div>
          <span className="text-[10px] text-slate-400">↓ 14.5% vs Prior Quarter</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Blended ROAS Multiplier</span>
          <div className="text-2xl font-bold text-white">14.8x</div>
          <span className="text-[10px] text-emerald-400">$14.80 Return per $1.00 Ad Spend</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Lead to Opportunity Conv.</span>
          <div className="text-2xl font-bold text-white">18.4%</div>
          <span className="text-[10px] text-emerald-400">Top Quartile B2B Funnel</span>
        </div>
      </div>
    </div>
  );
};
