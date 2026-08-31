import React, { useState } from "react";
import { AlertTriangle, RefreshCw, TrendingDown, Target, CheckCircle2 } from "lucide-react";

export const EnterpriseCreativeFatigueRadar: React.FC = () => {
  const ads = [
    { title: "LinkedIn B2B CPQ Interactive Demo Ad", ctrDrop: "-34.2% CTR", cpaRise: "+41.5% CPA", status: "Fatigued (Action Needed)" },
    { title: "Google Search: Enterprise CRM Alternative", ctrDrop: "-4.1% CTR", cpaRise: "+1.2% CPA", status: "High Efficiency" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Target className="w-5 h-5 text-emerald-400" />
            Ad Creative Fatigue & CPA Decay Radar
          </h3>
          <p className="text-xs text-slate-400">Automated detection of declining CTRs and rising customer acquisition costs</p>
        </div>
      </div>

      <div className="space-y-3">
        {ads.map((ad, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{ad.title}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">{ad.ctrDrop} • {ad.cpaRise}</div>
            </div>
            <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${
              ad.status.includes("Fatigued") ? "bg-amber-950 text-amber-400 border border-amber-800" : "bg-emerald-950 text-emerald-400 border border-emerald-800"
            }`}>
              {ad.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
