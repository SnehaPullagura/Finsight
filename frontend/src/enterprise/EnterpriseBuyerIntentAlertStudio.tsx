import React, { useState } from "react";
import { Zap, Bell, CheckCircle2, Clock } from "lucide-react";

export const EnterpriseBuyerIntentAlertStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Zap className="w-5 h-5 text-amber-400" />
            Real-Time Buyer Intent Trigger & Hot Deal Alert Engine
          </h3>
          <p className="text-xs text-slate-400">Sub-second notifications dispatched when economic buyers review pricing and legal terms</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Live Triggers Active
        </span>
      </div>

      <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold text-white">Live Buyer Event: Bruce Wayne (CEO) viewing Pricing Table</span>
          <span className="text-xs text-emerald-400 font-semibold">Active Now (3m 42s dwell)</span>
        </div>
        <div className="space-y-2 text-xs text-slate-300">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>P1 alert sent to Slack #deals-wayne-enterprises & Lead AE phone</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>Recommended action: Send personalized follow-up SMS with custom concession ramp</span>
          </div>
        </div>
      </div>
    </div>
  );
};
