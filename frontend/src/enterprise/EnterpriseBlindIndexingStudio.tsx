import React, { useState } from "react";
import { Search, Lock, Shield, CheckCircle2 } from "lucide-react";

export const EnterpriseBlindIndexingStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Search className="w-5 h-5 text-emerald-400" />
            Zero-Knowledge Encrypted Field Blind Indexing
          </h3>
          <p className="text-xs text-slate-400">Exact match searching over encrypted sensitive fields without leaking plaintext or cipher patterns</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          HMAC-SHA256 Blind Indexing
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Search Index Key</span>
          <div className="text-xs font-mono text-emerald-400">KDF-HMAC-256</div>
          <span className="text-[10px] text-slate-400">Isolated Search Salt</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Search Performance</span>
          <div className="text-2xl font-bold text-white">0.2ms</div>
          <span className="text-[10px] text-emerald-400">B-Tree Indexed Hash Lookup</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Zero-Knowledge Proof</span>
          <div className="text-xs font-bold text-emerald-400">100% Blind Search</div>
          <span className="text-[10px] text-slate-400">Zero Plaintext Leakage to DB</span>
        </div>
      </div>
    </div>
  );
};
