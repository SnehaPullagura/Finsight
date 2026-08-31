import React, { useState } from "react";
import { RefreshCw, Database, CheckCircle2, Zap } from "lucide-react";

export const EnterpriseSalesforceCDCStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <RefreshCw className="w-5 h-5 text-emerald-400" />
            Salesforce Bi-Directional CDC Sync & Event Bus
          </h3>
          <p className="text-xs text-slate-400">Zero-data-loss streaming synchronization with Salesforce Pub/Sub API and idempotency locking</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Streaming Active
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Replication Latency</span>
          <div className="text-2xl font-bold text-emerald-400">&lt; 250 ms</div>
          <span className="text-[10px] text-emerald-400">Sub-Second Bi-Directional Sync</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Events Synced Today</span>
          <div className="text-2xl font-bold text-white">48,250 Events</div>
          <span className="text-[10px] text-slate-400">100% Conflict Free</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Idempotency Guard</span>
          <div className="text-2xl font-bold text-white">SHA-256 Lock</div>
          <span className="text-[10px] text-slate-400">Duplicate Delivery Prevention</span>
        </div>
      </div>
    </div>
  );
};
