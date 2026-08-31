import React, { useState } from "react";
import { Zap, Clock, TrendingUp, AlertTriangle, CheckCircle2 } from "lucide-react";

export const EnterprisePipelineVelocityHeatmap: React.FC = () => {
  const stages = [
    { name: "Discovery", avgDays: 4.2, benchmark: 5.0, status: "healthy" },
    { name: "Scoping & Architecture", avgDays: 8.5, benchmark: 7.0, status: "warning" },
    { name: "Proposal & Pricing", avgDays: 5.1, benchmark: 6.0, status: "healthy" },
    { name: "Executive Negotiation", avgDays: 14.8, benchmark: 10.0, status: "critical" },
    { name: "Legal & Procurement", avgDays: 12.0, benchmark: 14.0, status: "healthy" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Zap className="w-5 h-5 text-emerald-400" />
            Deal Stage Velocity & Stagnation Heatmap
          </h3>
          <p className="text-xs text-slate-400">Identify pipeline friction points and stage stagnation bottlenecks across sales cycles</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
        {stages.map((stg, idx) => (
          <div key={idx} className={`p-4 rounded-xl border ${
            stg.status === "critical" ? "bg-red-950/30 border-red-800" :
            stg.status === "warning" ? "bg-amber-950/30 border-amber-800" : "bg-slate-950 border-slate-800"
          }`}>
            <span className="text-[11px] text-slate-400 font-semibold block">{stg.name}</span>
            <div className="text-xl font-bold text-white mt-1">{stg.avgDays} Days</div>
            <div className="text-[10px] text-slate-500 mt-2 flex justify-between">
              <span>Goal: {stg.benchmark}d</span>
              <span className={stg.status === "critical" ? "text-red-400 font-bold" : stg.status === "warning" ? "text-amber-400" : "text-emerald-400"}>
                {stg.status.toUpperCase()}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
