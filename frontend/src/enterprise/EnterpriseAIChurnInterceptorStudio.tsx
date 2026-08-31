import React, { useState } from "react";
import { ShieldAlert, Zap, CheckCircle2, HeartPulse } from "lucide-react";

export const EnterpriseAIChurnInterceptorStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Zap className="w-5 h-5 text-emerald-400" />
            Real-Time Automated Churn Interception Engine
          </h3>
          <p className="text-xs text-slate-400">Zero-latency automated counter-churn offer dispatch upon detection of telemetry anomalies</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Interceptor Active
        </span>
      </div>

      <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold text-white">Active Interception: Cyberdyne Systems ($140,000 ARR)</span>
          <span className="text-xs text-emerald-400 font-semibold">Triage Engaged</span>
        </div>
        <div className="space-y-2 text-xs text-slate-300">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>Proactive senior solutions architect hotline assigned</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>Feature optimization & workflow review scheduled</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>1-year price lock offered upon early agreement execution</span>
          </div>
        </div>
      </div>
    </div>
  );
};
