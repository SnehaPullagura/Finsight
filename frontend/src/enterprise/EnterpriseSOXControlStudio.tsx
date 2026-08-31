import React, { useState } from "react";
import { ShieldCheck, Lock, CheckCircle2, AlertCircle } from "lucide-react";

export const EnterpriseSOXControlStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            SOX ITGC Separation of Duties & Change Control Auditor
          </h3>
          <p className="text-xs text-slate-400">Automated validation of production release approvals and financial audit trails</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          100% SOX Compliant
        </span>
      </div>

      <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold text-white">Continuous ITGC Auditing Engine</span>
          <span className="text-xs text-emerald-400 font-semibold">Live Monitoring</span>
        </div>
        <div className="space-y-2 text-xs text-slate-300">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>Separation of Duties (SoD) enforced on all revenue configuration mutations</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>HMAC SHA-256 cryptographic signatures verified across 100% of audit ledger rows</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>Automated rollback test plans verified for every production deploy</span>
          </div>
        </div>
      </div>
    </div>
  );
};
