import React, { useState } from "react";
import { DollarSign, Award, TrendingUp, CheckCircle2 } from "lucide-react";

export const EnterpriseRepHiringPaybackStudio: React.FC = () => {
  const reps = [
    { name: "Alex Vance", tenure: "9 Mo", cost: "$168,750", margin: "$480,000", roi: "2.84x", status: "Payback Achieved" },
    { name: "Sarah Connor", tenure: "8 Mo", cost: "$150,000", margin: "$420,000", roi: "2.80x", status: "Payback Achieved" },
    { name: "John Wick", tenure: "6 Mo", cost: "$112,500", margin: "$85,000", roi: "0.75x", status: "In Payback Runway" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <DollarSign className="w-5 h-5 text-emerald-400" />
            Sales Rep Hiring Payback & Gross Margin Contribution
          </h3>
          <p className="text-xs text-slate-400">Fully loaded rep cost vs cumulative closed gross margin generated</p>
        </div>
      </div>

      <div className="space-y-3">
        {reps.map((r, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{r.name} ({r.tenure})</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Fully Loaded Cost: {r.cost} → Margin: {r.margin}</div>
            </div>
            <div className="text-right">
              <span className="text-sm font-bold text-emerald-400">{r.roi} ROI</span>
              <span className="text-[10px] text-slate-500 block">{r.status}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
