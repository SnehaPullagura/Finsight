import React, { useState } from "react";
import { UserCheck, Award, TrendingUp, CheckCircle2 } from "lucide-react";

export const EnterpriseRepRampMilestoneStudio: React.FC = () => {
  const reps = [
    { name: "Jessica Alba", tenure: "2 Months", built: "$145,000", target: "$100,000", pacing: "145.0%", status: "Ahead of Schedule" },
    { name: "Marcus Wright", tenure: "4 Months", built: "$280,000", target: "$300,000", pacing: "93.3%", status: "On Track" },
    { name: "Kyle Reese", tenure: "5 Months", built: "$180,000", target: "$300,000", pacing: "60.0%", status: "Needs Ramp Coaching" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <UserCheck className="w-5 h-5 text-emerald-400" />
            New Sales Hire Ramp Velocity & Milestone Pacing
          </h3>
          <p className="text-xs text-slate-400">Tracks pipeline generation benchmarks and deal closing pacing during initial 6-month ramp</p>
        </div>
      </div>

      <div className="space-y-3">
        {reps.map((r, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{r.name} ({r.tenure})</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Pipeline Built: {r.built} / {r.target} Benchmark</div>
            </div>
            <div className="text-right">
              <span className="text-sm font-bold text-emerald-400">{r.pacing} Pacing</span>
              <span className="text-[10px] text-slate-500 block">{r.status}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
