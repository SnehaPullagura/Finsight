import React, { useState } from "react";
import { Users, Sparkles, CheckCircle2, Award } from "lucide-react";

export const EnterpriseChampionRadarStudio: React.FC = () => {
  const champions = [
    { user: "bruce.wayne@wayne.internal", account: "Wayne Enterprises", role: "Executive Sponsor", nps: "10/10", sessions: "48 / mo" },
    { user: "tony.stark@stark.internal", account: "Stark Industries", role: "Product Power Champion", nps: "10/10", sessions: "62 / mo" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-emerald-400" />
            Customer Champion & Executive Sponsor Advocacy Radar
          </h3>
          <p className="text-xs text-slate-400">Identifies high-NPS power users and executive sponsors primed for expansion co-pitching</p>
        </div>
      </div>

      <div className="space-y-3">
        {champions.map((c, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{c.user} ({c.account})</div>
              <div className="text-[11px] text-slate-400 mt-0.5">NPS: {c.nps} • {c.sessions}</div>
            </div>
            <span className="text-xs text-emerald-400 font-semibold bg-emerald-950 border border-emerald-800 px-2.5 py-1 rounded-full">
              {c.role}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
