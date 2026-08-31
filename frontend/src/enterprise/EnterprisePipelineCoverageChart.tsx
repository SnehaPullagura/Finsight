import React, { useState } from "react";
import { Target, CheckCircle2, AlertTriangle, Users } from "lucide-react";

export const EnterprisePipelineCoverageChart: React.FC = () => {
  const coverage = [
    { rep: "Alex Vance", quota: "$150,000", pipe: "$540,000", multiple: "3.6x", status: "Healthy" },
    { rep: "Sarah Connor", quota: "$200,000", pipe: "$620,000", multiple: "3.1x", status: "Healthy" },
    { rep: "John Wick", quota: "$120,000", pipe: "$210,000", multiple: "1.8x", status: "At Risk" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Target className="w-5 h-5 text-emerald-400" />
            Sales Rep Pipeline Quota Coverage Ratio
          </h3>
          <p className="text-xs text-slate-400">Track 3.0x+ pipeline coverage targets across sales team members</p>
        </div>
      </div>

      <div className="space-y-3">
        {coverage.map((c, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{c.rep}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">
                Remaining Quota: {c.quota} • Open Pipeline: {c.pipe}
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="text-right">
                <span className="text-sm font-bold text-white">{c.multiple}</span>
                <span className="text-[10px] text-slate-500 block">Coverage</span>
              </div>
              <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${
                c.status === "Healthy" ? "bg-emerald-950 text-emerald-400 border border-emerald-800" : "bg-red-950 text-red-400 border border-red-800"
              }`}>
                {c.status}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
