import React, { useState } from "react";
import { DollarSign, TrendingUp, Target, Award } from "lucide-react";

export const EnterpriseChannelLTVToCACStudio: React.FC = () => {
  const channels = [
    { name: "Direct Executive Outreach", cac: "$1,250", ltv: "$14,500", ratio: "11.6x", rating: "Top Decile" },
    { name: "Google High-Intent Search", cac: "$1,850", ltv: "$11,200", ratio: "6.1x", rating: "Top Decile" },
    { name: "LinkedIn Sponsored Content", cac: "$2,800", ltv: "$9,800", ratio: "3.5x", rating: "Healthy" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Target className="w-5 h-5 text-emerald-400" />
            Marketing Channel LTV : CAC Unit Economics
          </h3>
          <p className="text-xs text-slate-400">Measure capital efficiency and scalable acquisition channels</p>
        </div>
      </div>

      <div className="space-y-3">
        {channels.map((ch, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{ch.name}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">CAC: {ch.cac} • LTV: {ch.ltv}</div>
            </div>
            <div className="text-right">
              <span className="text-sm font-bold text-emerald-400">{ch.ratio}</span>
              <span className="text-[10px] text-slate-500 block">{ch.rating}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
