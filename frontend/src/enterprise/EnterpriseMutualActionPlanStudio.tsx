import React, { useState } from "react";
import { CheckSquare, Calendar, CheckCircle2, Clock } from "lucide-react";

export const EnterpriseMutualActionPlanStudio: React.FC = () => {
  const milestones = [
    { title: "Technical Architecture & Security Review", date: "Sept 12", owner: "Wayne InfoSec Lead", status: "Completed" },
    { title: "CPQ Custom Quote & Terms Approval", date: "Sept 18", owner: "ClientFlow Deal Desk", status: "Completed" },
    { title: "Executive Sponsor Sign-Off & eSignature", date: "Sept 25", owner: "Bruce Wayne (CEO)", status: "In Progress" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <CheckSquare className="w-5 h-5 text-emerald-400" />
            Joint Evaluation Mutual Action Plan (MAP)
          </h3>
          <p className="text-xs text-slate-400">Shared milestone calendar synchronizing buyer and seller decision gates</p>
        </div>
      </div>

      <div className="space-y-3">
        {milestones.map((m, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{m.title}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Due: {m.date} • Owner: {m.owner}</div>
            </div>
            <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${
              m.status === "Completed" ? "bg-emerald-950 text-emerald-400 border border-emerald-800" : "bg-blue-950 text-blue-400 border border-blue-800"
            }`}>
              {m.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
