import React, { useState } from "react";
import { TrendingUp, Users, Target, CheckCircle2 } from "lucide-react";

export const EnterprisePipelineGenVelocityStudio: React.FC = () => {
  const reps = [
    { name: "Alex Vance", created: "$950,000", quota: "$250,000", multiple: "3.8x", selfSourced: "65%", tier: "Self-Sustaining" },
    { name: "Sarah Connor", created: "$1,200,000", quota: "$250,000", multiple: "4.8x", selfSourced: "72%", tier: "High Engine" },
    { name: "John Wick", created: "$540,000", quota: "$250,000", multiple: "2.1x", selfSourced: "30%", tier: "Inbound Dependent" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Target className="w-5 h-5 text-emerald-400" />
            Sales Rep Outbound Pipeline Generation Velocity
          </h3>
          <p className="text-xs text-slate-400">Quarterly new pipeline creation multiple and self-sourced outbound ratio</p>
        </div>
      </div>

      <div className="space-y-3">
        {reps.map((r, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{r.name}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Created: {r.created} • Self-Sourced: {r.selfSourced}</div>
            </div>
            <div className="text-right">
              <span className="text-sm font-bold text-emerald-400">{r.multiple} Quota Coverage</span>
              <span className="text-[10px] text-slate-500 block">{r.tier}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
