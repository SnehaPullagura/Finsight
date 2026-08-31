import React, { useState } from "react";
import { TrendingDown, Target, DollarSign, CheckCircle2 } from "lucide-react";

export const EnterpriseCreativeROIDecayStudio: React.FC = () => {
  const schedule = [
    { week: "Week 1", roas: "12.4x", status: "Highly Profitable" },
    { week: "Week 2", roas: "11.8x", status: "Highly Profitable" },
    { week: "Week 4", roas: "10.6x", status: "Profitable" },
    { week: "Week 6", roas: "9.2x", status: "Profitable" },
    { week: "Week 8", roas: "7.8x", status: "Healthy / Schedule Refresh" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Target className="w-5 h-5 text-emerald-400" />
            Ad Creative ROAS Decay Trajectory Modeler
          </h3>
          <p className="text-xs text-slate-400">Projected weekly degradation of creative ROAS under constant audience frequency exposure</p>
        </div>
      </div>

      <div className="space-y-3">
        {schedule.map((s, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{s.week}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Projected ROAS: <span className="text-emerald-400 font-bold">{s.roas}</span></div>
            </div>
            <span className="text-xs text-slate-400 font-semibold">{s.status}</span>
          </div>
        ))}
      </div>
    </div>
  );
};
