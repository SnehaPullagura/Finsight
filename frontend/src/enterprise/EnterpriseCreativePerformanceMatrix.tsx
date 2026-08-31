import React, { useState } from "react";
import { Target, TrendingUp, DollarSign, Award, CheckCircle2 } from "lucide-react";

export const EnterpriseCreativePerformanceMatrix: React.FC = () => {
  const creatives = [
    { name: "Executive CPQ Interactive Product Tour", format: "Interactive Video", roas: "12.4x", ctr: "3.8%", cpc: "$4.12", tier: "Top Performer" },
    { name: "Multi-Tenant Enterprise Security Benchmark", format: "PDF Whitepaper", roas: "8.6x", ctr: "2.9%", cpc: "$5.80", tier: "Top Performer" },
    { name: "Salesforce Migration TCO Calculator", format: "Web Calculator", roas: "5.2x", ctr: "2.1%", cpc: "$7.20", tier: "Solid" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Target className="w-5 h-5 text-emerald-400" />
            Marketing Creative Performance & Return on Ad Spend (ROAS)
          </h3>
          <p className="text-xs text-slate-400">Attributed pipeline revenue multipliers by ad creative and interactive asset</p>
        </div>
      </div>

      <div className="space-y-3">
        {creatives.map((c, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{c.name}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Format: {c.format} • CTR: {c.ctr} • CPC: {c.cpc}</div>
            </div>
            <div className="text-right">
              <span className="text-sm font-bold text-emerald-400">{c.roas} ROAS</span>
              <span className="text-[10px] text-slate-500 block">{c.tier}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
