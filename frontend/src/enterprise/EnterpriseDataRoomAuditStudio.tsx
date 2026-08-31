import React, { useState } from "react";
import { ShieldCheck, FileText, Lock, CheckCircle2, History } from "lucide-react";

export const EnterpriseDataRoomAuditStudio: React.FC = () => {
  const events = [
    { user: "cfo@stark.internal", doc: "ClientFlow Enterprise CPQ Quote.pdf", action: "Downloaded (Dynamic Watermarked)", time: "12m ago" },
    { user: "infosec@wayne.internal", doc: "SOC-2 Type II Report 2026.pdf", action: "Viewed Page 1-14", time: "45m ago" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Lock className="w-5 h-5 text-emerald-400" />
            Virtual Data Room (VDR) Cryptographic Audit Trail
          </h3>
          <p className="text-xs text-slate-400">Immutable ledger of buyer document downloads with dynamic IP/viewer watermarking</p>
        </div>
      </div>

      <div className="space-y-3">
        {events.map((e, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{e.doc}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Viewer: {e.user} • Action: <span className="text-emerald-400 font-semibold">{e.action}</span></div>
            </div>
            <span className="text-xs text-slate-500 font-semibold">{e.time}</span>
          </div>
        ))}
      </div>
    </div>
  );
};
