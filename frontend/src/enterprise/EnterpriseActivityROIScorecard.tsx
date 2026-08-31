import React, { useState } from "react";
import { Activity, DollarSign, Award, TrendingUp, CheckCircle2 } from "lucide-react";

export const EnterpriseActivityROIScorecard: React.FC = () => {
  const reps = [
    { name: "Alex Vance", activities: 240, wonRev: "$280,000", revPerAct: "$1,166", demoConv: "48.5%", rating: "High Leverage" },
    { name: "Sarah Connor", activities: 380, wonRev: "$310,000", revPerAct: "$815", demoConv: "42.0%", rating: "High Leverage" },
    { name: "John Wick", activities: 410, wonRev: "$140,000", revPerAct: "$341", demoConv: "24.0%", rating: "Solid Contributor" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Activity className="w-5 h-5 text-emerald-400" />
            Sales Rep Activity ROI & Conversion Efficiency
          </h3>
          <p className="text-xs text-slate-400">Revenue generated per sales touchpoint and demo-to-close win rates</p>
        </div>
      </div>

      <div className="space-y-3">
        {reps.map((r, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{r.name}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">
                {r.activities} activities • {r.wonRev} Won • Demo Close: {r.demoConv}
              </div>
            </div>
            <div className="text-right">
              <span className="text-sm font-bold text-emerald-400">{r.revPerAct} / Activity</span>
              <span className="text-[10px] text-slate-500 block">{r.rating}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
