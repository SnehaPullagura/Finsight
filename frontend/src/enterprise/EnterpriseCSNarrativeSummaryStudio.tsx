import React, { useState } from "react";
import { Sparkles, HeartPulse, CheckCircle2, MessageSquare } from "lucide-react";

export const EnterpriseCSNarrativeSummaryStudio: React.FC = () => {
  const narratives = [
    { name: "Acme Global Industries", health: 95, narrative: "Acme Global is an elite champion account (95/100) with strong NPS (10/10) and expanding ARR ($320k).", urgency: "Low" },
    { name: "Cyberdyne Systems", health: 48, narrative: "Cyberdyne Systems is at elevated risk (48/100). Executive outreach and dedicated technical triage recommended.", urgency: "High" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-emerald-400" />
            AI Prescriptive Account Health Narratives
          </h3>
          <p className="text-xs text-slate-400">Automated natural language executive briefings synthesized from telemetry and support tickets</p>
        </div>
      </div>

      <div className="space-y-3">
        {narratives.map((n, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-white">{n.name}</span>
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                n.urgency === "High" ? "bg-red-950 text-red-400 border border-red-800" : "bg-emerald-950 text-emerald-400 border border-emerald-800"
              }`}>
                {n.urgency} Urgency
              </span>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">{n.narrative}</p>
          </div>
        ))}
      </div>
    </div>
  );
};
