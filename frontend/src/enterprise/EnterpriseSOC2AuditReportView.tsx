import React, { useState } from "react";
import { ShieldCheck, CheckCircle2, Award, Lock, FileText } from "lucide-react";

export const EnterpriseSOC2AuditReportView: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            SOC 2 Type II & Security Compliance Attestation
          </h3>
          <p className="text-xs text-slate-400">Verified security trust criteria with zero compliance exceptions</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Unqualified Clean Opinion
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Security (CC1-9)</span>
          <div className="text-lg font-bold text-emerald-400">48 / 48 Tested</div>
          <span className="text-[10px] text-slate-400">0 Exceptions</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Availability</span>
          <div className="text-lg font-bold text-white">99.98% Uptime</div>
          <span className="text-[10px] text-emerald-400">SLA Exceeded</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Confidentiality</span>
          <div className="text-lg font-bold text-white">AES-256-GCM</div>
          <span className="text-[10px] text-emerald-400">Field Encrypted</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Privacy (P1-8)</span>
          <div className="text-lg font-bold text-white">GDPR Compliant</div>
          <span className="text-[10px] text-emerald-400">&lt; 48hr DSR SLA</span>
        </div>
      </div>
    </div>
  );
};
