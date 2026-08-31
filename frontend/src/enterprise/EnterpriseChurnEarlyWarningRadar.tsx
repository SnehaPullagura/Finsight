import React, { useState } from "react";
import { AlertTriangle, Clock, ShieldAlert, CheckCircle2 } from "lucide-react";

export const EnterpriseChurnEarlyWarningRadar: React.FC = () => {
  const atRisk = [
    { name: "Umbrella Health Systems", arr: "$120,000", drop: "-42% DAU", nps: "5/10 (Detractor)", risk: "Critical" },
    { name: "Initech Enterprise", arr: "$85,000", drop: "-28% DAU", nps: "6/10 (Detractor)", risk: "Elevated" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-red-400" />
            Proactive Account Churn Early Warning Radar
          </h3>
          <p className="text-xs text-slate-400">Multi-signal telemetry analyzing telemetry drops and detractor NPS scores</p>
        </div>
      </div>

      <div className="space-y-3">
        {atRisk.map((a, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{a.name}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">
                ARR: {a.arr} • Signal: {a.drop} • Survey: {a.nps}
              </div>
            </div>
            <span className={`text-xs font-bold px-2.5 py-1 rounded-full ${
              a.risk === "Critical" ? "bg-red-950 text-red-400 border border-red-800" : "bg-amber-950 text-amber-400 border border-amber-800"
            }`}>
              {a.risk}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
