import React, { useState } from "react";
import { TrendingUp, DollarSign, CheckCircle2, Award } from "lucide-react";

export const EnterpriseRepPaybackScheduleStudio: React.FC = () => {
  const curve = [
    { month: "Month 1", cost: "$18,750", margin: "$0", net: "-$18,750", status: "Ramping" },
    { month: "Month 3", cost: "$56,250", margin: "$25,000", net: "-$31,250", status: "Ramping" },
    { month: "Month 6", cost: "$112,500", margin: "$120,000", net: "+$7,500", status: "Payback Hit" },
    { month: "Month 9", cost: "$168,750", margin: "$280,000", net: "+$111,250", status: "Highly Profitable" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-emerald-400" />
            Monthly Sales Rep Hiring Payback Schedule
          </h3>
          <p className="text-xs text-slate-400">Cumulative fully-loaded compensation against gross profit margin contribution curve</p>
        </div>
      </div>

      <div className="space-y-3">
        {curve.map((c, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{c.month}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Cumulative Cost: {c.cost} • Margin: {c.margin}</div>
            </div>
            <div className="text-right">
              <span className={`text-sm font-bold ${c.net.startsWith("+") ? "text-emerald-400" : "text-amber-400"}`}>{c.net}</span>
              <span className="text-[10px] text-slate-500 block">{c.status}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
