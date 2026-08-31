import React, { useState } from "react";
import { Award, PieChart, CheckCircle2, XCircle } from "lucide-react";

export const EnterpriseWinLossAnalysisStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <PieChart className="w-5 h-5 text-emerald-400" />
            Win / Loss Decision Matrix & Competitor Insights
          </h3>
          <p className="text-xs text-slate-400">Quantitative reasons for closed won and closed lost opportunities</p>
        </div>
        <div className="text-right">
          <span className="text-[11px] text-slate-400">Quarterly Win Rate</span>
          <div className="text-xl font-bold text-emerald-400">68.4%</div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-2">
          <span className="text-xs font-bold text-emerald-400 flex items-center gap-1.5">
            <CheckCircle2 className="w-4 h-4" /> Top Drivers for Closed Won
          </span>
          <ul className="space-y-1.5 text-xs text-slate-300">
            <li>1. Superior DAG Workflow Customization (42%)</li>
            <li>2. Out-of-the-Box Multi-Tenant Security (28%)</li>
            <li>3. Transparent Predictable CPQ Pricing (18%)</li>
          </ul>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-2">
          <span className="text-xs font-bold text-red-400 flex items-center gap-1.5">
            <XCircle className="w-4 h-4" /> Top Drivers for Closed Lost
          </span>
          <ul className="space-y-1.5 text-xs text-slate-300">
            <li>1. Budget Freeze / Economic Headwinds (50%)</li>
            <li>2. Preferred Existing Legacy Vendor (30%)</li>
            <li>3. Implementation Timeline Fit (20%)</li>
          </ul>
        </div>
      </div>
    </div>
  );
};
