import React, { useState } from "react";
import { GitCommit, Compass, CheckCircle2, TrendingUp } from "lucide-react";

export const EnterpriseBuyerJourneyMapStudio: React.FC = () => {
  const steps = [
    { title: "First Touch: Google Search Ad -> CPQ Interactive Product Tour", date: "Aug 12", channel: "Paid Search" },
    { title: "Discovery Call & Custom Architecture Scoping Sandbox", date: "Aug 19", channel: "Direct AE" },
    { title: "InfoSec DSR Access & SOC2 Type II Report Download", date: "Aug 26", channel: "Digital Sales Room" },
    { title: "Executive Proposal View & Mutual Action Plan Agreement", date: "Sept 01", channel: "Executive Sync" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Compass className="w-5 h-5 text-emerald-400" />
            Full-Funnel Buyer Journey Reconstructor
          </h3>
          <p className="text-xs text-slate-400">Chronological multi-touch journey attribution mapping every buyer touchpoint</p>
        </div>
      </div>

      <div className="space-y-3">
        {steps.map((s, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{s.title}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Date: {s.date} • Channel: {s.channel}</div>
            </div>
            <span className="text-xs text-emerald-400 font-semibold bg-emerald-950 border border-emerald-800 px-2.5 py-1 rounded-full">
              Touchpoint #{idx + 1}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
