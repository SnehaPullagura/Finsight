import React, { useState } from "react";
import { TrendingUp, Users, DollarSign, CheckCircle2, ChevronRight } from "lucide-react";

export const EnterpriseExpansionOpportunityMatrix: React.FC = () => {
  const candidates = [
    { name: "Wayne Enterprises", utilization: "98%", health: "95 / 100", currentArr: "$250,000", expansionArr: "+$62,500" },
    { name: "Stark Industries", utilization: "94%", health: "92 / 100", currentArr: "$180,000", expansionArr: "+$45,000" },
    { name: "Cyberdyne Systems", utilization: "91%", health: "88 / 100", currentArr: "$95,000", expansionArr: "+$23,750" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-emerald-400" />
            Customer Expansion & Upsell Opportunity Radar
          </h3>
          <p className="text-xs text-slate-400">High-health accounts approaching seat capacity thresholds</p>
        </div>
      </div>

      <div className="space-y-3">
        {candidates.map((c, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{c.name}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">
                License Utilization: {c.utilization} • Health Score: {c.health} • Base ARR: {c.currentArr}
              </div>
            </div>
            <div className="text-right">
              <span className="text-[10px] text-slate-500 uppercase font-semibold">Expansion Potential</span>
              <div className="text-sm font-bold text-emerald-400">{c.expansionArr}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
