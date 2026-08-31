import React, { useState } from "react";
import { Calendar, CheckCircle2, Clock, AlertTriangle, ChevronRight } from "lucide-react";

interface MilestoneTask {
  id: string;
  name: string;
  owner: string;
  start_day: number;
  duration_days: number;
  progress_pct: number;
  status: "completed" | "in_progress" | "pending";
}

const SAMPLE_MILESTONES: MilestoneTask[] = [
  { id: "m1", name: "Security & SAML SSO Configuration", owner: "Alexander Vance", start_day: 1, duration_days: 7, progress_pct: 100, status: "completed" },
  { id: "m2", name: "Contact & Account Data Migration", owner: "Sarah Connor", start_day: 5, duration_days: 10, progress_pct: 75, status: "in_progress" },
  { id: "m3", name: "Custom Workflow DAG Automation Setup", owner: "Alexander Vance", start_day: 12, duration_days: 8, progress_pct: 30, status: "in_progress" },
  { id: "m4", name: "Executive Team User Training & Onboarding", owner: "Pepper Potts", start_day: 18, duration_days: 12, progress_pct: 0, status: "pending" }
];

export const AdvancedGanttChart: React.FC = () => {
  const [tasks] = useState<MilestoneTask[]>(SAMPLE_MILESTONES);
  const totalDays = 30;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Calendar className="w-5 h-5 text-emerald-400" />
            Customer Onboarding Milestone & Gantt Timeline
          </h3>
          <p className="text-xs text-slate-400">Track implementation schedules, critical paths, and milestone deliverables</p>
        </div>
      </div>

      <div className="space-y-3">
        {tasks.map(task => {
          const leftPct = (task.start_day / totalDays) * 100;
          const widthPct = (task.duration_days / totalDays) * 100;

          return (
            <div key={task.id} className="space-y-1 text-xs">
              <div className="flex items-center justify-between">
                <div className="font-semibold text-white flex items-center gap-2">
                  <span className={`w-2 h-2 rounded-full ${
                    task.status === "completed" ? "bg-emerald-400" :
                    task.status === "in_progress" ? "bg-blue-400" : "bg-slate-600"
                  }`} />
                  <span>{task.name}</span>
                </div>
                <div className="text-[11px] text-slate-400">
                  {task.owner} — <strong className="text-emerald-400">{task.progress_pct}%</strong>
                </div>
              </div>

              <div className="h-6 bg-slate-950 rounded-lg relative overflow-hidden border border-slate-800">
                <div
                  style={{ left: `${leftPct}%`, width: `${widthPct}%` }}
                  className={`absolute top-1 bottom-1 rounded-md px-2 flex items-center text-[10px] font-bold text-slate-950 transition-all ${
                    task.status === "completed" ? "bg-emerald-400" :
                    task.status === "in_progress" ? "bg-blue-400" : "bg-slate-700 text-white"
                  }`}
                >
                  <span className="truncate">{task.duration_days}d</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
