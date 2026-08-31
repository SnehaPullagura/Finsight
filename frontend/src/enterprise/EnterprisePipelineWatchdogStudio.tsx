import React, { useState } from "react";
import { AlertCircle, Clock, ShieldAlert, CheckCircle2 } from "lucide-react";

export const EnterprisePipelineWatchdogStudio: React.FC = () => {
  const stagnant = [
    { name: "Oscorp Holdings MSA", value: "$95,000", days: 28, rep: "John Wick", severity: "Warning" },
    { name: "Cyberdyne Systems AI Expansion", value: "$45,000", days: 34, rep: "John Wick", severity: "Critical" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Clock className="w-5 h-5 text-amber-400" />
            Deal Stagnation & Pipeline Inactivity Watchdog
          </h3>
          <p className="text-xs text-slate-400">Automated alerts for enterprise opportunities without recorded touchpoints over 14+ days</p>
        </div>
      </div>

      <div className="space-y-3">
        {stagnant.map((s, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{s.name} ({s.value})</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Owner: {s.rep} • {s.days} days with zero customer activity</div>
            </div>
            <span className={`text-xs font-bold px-2.5 py-1 rounded-full ${
              s.severity === "Critical" ? "bg-red-950 text-red-400 border border-red-800" : "bg-amber-950 text-amber-400 border border-amber-800"
            }`}>
              {s.severity}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
