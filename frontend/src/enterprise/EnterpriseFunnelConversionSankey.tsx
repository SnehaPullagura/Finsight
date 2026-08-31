import React, { useState } from "react";
import { Filter, TrendingUp, CheckCircle2, ArrowRight } from "lucide-react";

export const EnterpriseFunnelConversionSankey: React.FC = () => {
  const steps = [
    { name: "Website Visitors", count: "125,000", conv: "2.4% to Lead" },
    { name: "Inbound Leads", count: "3,000", conv: "45.0% to MQL" },
    { name: "Marketing Qualified (MQL)", count: "1,350", conv: "52.0% to SQL" },
    { name: "Sales Qualified (SQL)", count: "702", conv: "38.0% to Opp" },
    { name: "Opportunities", count: "266", conv: "32.0% to Won" },
    { name: "Closed Won Customers", count: "85", conv: "100%" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Filter className="w-5 h-5 text-emerald-400" />
            Full-Funnel Sales & Marketing Velocity Pipeline
          </h3>
          <p className="text-xs text-slate-400">End-to-end stage conversion rates from visitor acquisition to closed-won revenue</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-6 gap-2">
        {steps.map((st, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-3 rounded-xl space-y-1">
            <span className="text-[10px] text-slate-400 font-semibold uppercase truncate block">{st.name}</span>
            <div className="text-lg font-bold text-white">{st.count}</div>
            <span className="text-[10px] text-emerald-400 font-medium block">{st.conv}</span>
          </div>
        ))}
      </div>
    </div>
  );
};
