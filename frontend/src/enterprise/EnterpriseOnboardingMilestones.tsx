import React, { useState } from "react";
import { CheckCircle2, Circle, Clock, ArrowRight, ShieldCheck } from "lucide-react";

export const EnterpriseOnboardingMilestones: React.FC = () => {
  const milestones = [
    { title: "Kickoff & Architecture Review", day: "Day 1", completed: true },
    { title: "SSO & Identity Provider Verification", day: "Day 7", completed: true },
    { title: "Historical Data Migration & Mapping", day: "Day 14", completed: true },
    { title: "Sales Team Workflow Certification", day: "Day 21", completed: false },
    { title: "Executive Go-Live Sign-Off", day: "Day 30", completed: false }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            Enterprise White-Glove Onboarding Milestones
          </h3>
          <p className="text-xs text-slate-400">30-day time-to-value implementation milestones for enterprise accounts</p>
        </div>
        <span className="text-xs text-emerald-400 font-bold bg-emerald-950 border border-emerald-800 px-3 py-1 rounded-full">
          60% Completed (On Schedule)
        </span>
      </div>

      <div className="space-y-3">
        {milestones.map((m, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div className="flex items-center gap-3">
              {m.completed ? (
                <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
              ) : (
                <Circle className="w-5 h-5 text-slate-600 shrink-0" />
              )}
              <div>
                <div className={`text-xs font-bold ${m.completed ? "text-white" : "text-slate-400"}`}>{m.title}</div>
                <div className="text-[10px] text-slate-500">{m.day} Target</div>
              </div>
            </div>
            <span className={`text-xs font-semibold ${m.completed ? "text-emerald-400" : "text-slate-500"}`}>
              {m.completed ? "Completed" : "In Progress"}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
