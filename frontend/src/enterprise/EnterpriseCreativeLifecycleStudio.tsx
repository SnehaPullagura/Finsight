import React, { useState } from "react";
import { RefreshCw, Target, TrendingDown, CheckCircle2 } from "lucide-react";

export const EnterpriseCreativeLifecycleStudio: React.FC = () => {
  const creatives = [
    { name: "Executive CPQ Video Tour", days: 12, ctr: "3.8%", fatigue: "0%", stage: "Peak Performance" },
    { name: "Multi-Tenant Whitepaper Ad", days: 38, ctr: "2.9%", fatigue: "-8.5%", stage: "Maturity" },
    { name: "Legacy Migration Webinar", days: 54, ctr: "1.4%", fatigue: "-38.2%", stage: "Fatigued" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <RefreshCw className="w-5 h-5 text-emerald-400" />
            Ad Creative Lifecycle & Fatigue Staging Studio
          </h3>
          <p className="text-xs text-slate-400">Automated tracking of creative age, performance decay, and variant retirement</p>
        </div>
      </div>

      <div className="space-y-3">
        {creatives.map((c, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{c.name}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">{c.days} days active • Current CTR: {c.ctr} • Decay: {c.fatigue}</div>
            </div>
            <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${
              c.stage === "Peak Performance" ? "bg-emerald-950 text-emerald-400 border border-emerald-800" :
              c.stage === "Maturity" ? "bg-blue-950 text-blue-400 border border-blue-800" : "bg-amber-950 text-amber-400 border border-amber-800"
            }`}>
              {c.stage}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
