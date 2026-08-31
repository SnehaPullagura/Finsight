import React, { useState } from "react";
import { AlertTriangle, RefreshCw, CheckCircle2, DollarSign } from "lucide-react";

export const EnterpriseCreativeAlertQueueStudio: React.FC = () => {
  const alerts = [
    { title: "Legacy Migration Webinar Ad", cpa: "$142.50", inflation: "+54.2%", status: "Auto-Paused & Replaced" },
    { title: "Generic Enterprise CPQ Banner", cpa: "$98.00", inflation: "+38.4%", status: "Queued for Refresh" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-amber-400" />
            Ad Fatigue Real-Time Queue & Auto-Pause Guard
          </h3>
          <p className="text-xs text-slate-400">Automated budget protection pausing exhausted creatives with CPA spikes</p>
        </div>
      </div>

      <div className="space-y-3">
        {alerts.map((a, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{a.title}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Current CPA: {a.cpa} • CPA Spike: <span className="text-amber-400 font-bold">{a.inflation}</span></div>
            </div>
            <span className="text-xs text-emerald-400 font-semibold bg-emerald-950 border border-emerald-800 px-2.5 py-1 rounded-full">
              {a.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
