import React, { useState } from "react";
import { TrendingUp, Plus, DollarSign, CheckCircle2 } from "lucide-react";

export const EnterpriseExpansionPipelineStudio: React.FC = () => {
  const deals = [
    { title: "Wayne Enterprises — Expansion & Add-On", value: "$62,500", prob: "75%", stage: "Discovery" },
    { title: "Stark Industries — Additional 50 Seats", value: "$45,000", prob: "80%", stage: "Scoping" },
    { title: "Cyberdyne Systems — AI Copilot Expansion", value: "$23,750", prob: "70%", stage: "Discovery" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-emerald-400" />
            Automated Customer Success Expansion Pipeline
          </h3>
          <p className="text-xs text-slate-400">Auto-generated expansion pipeline opportunities triggered by telemetry thresholds</p>
        </div>
        <button className="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-500 text-white px-3 py-1.5 rounded-lg text-xs font-semibold shadow transition-colors">
          <Plus className="w-4 h-4" />
          Sync to CRM
        </button>
      </div>

      <div className="space-y-3">
        {deals.map((d, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{d.title}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Stage: {d.stage} • Probability: {d.prob}</div>
            </div>
            <div className="text-right">
              <span className="text-sm font-bold text-emerald-400">{d.value}</span>
              <span className="text-[10px] text-slate-500 block">Expansion ARR</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
