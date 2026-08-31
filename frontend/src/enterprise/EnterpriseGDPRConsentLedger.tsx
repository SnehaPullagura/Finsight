import React, { useState } from "react";
import { ShieldCheck, CheckCircle2, Lock, FileText, Search } from "lucide-react";

export const EnterpriseGDPRConsentLedger: React.FC = () => {
  const consents = [
    { contact: "alex.vance@initech.internal", type: "Data Processing (Art. 6)", status: "Granted", date: "2026-08-28 14:22:05" },
    { contact: "sarah.connor@stark.internal", type: "Marketing Communications", status: "Granted", date: "2026-08-25 09:15:30" },
    { contact: "bruce.wayne@wayne.internal", type: "Analytics & Telemetry", status: "Revoked", date: "2026-08-20 18:40:12" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            GDPR Article 7 Consent Ledger & Preference Center
          </h3>
          <p className="text-xs text-slate-400">Immutable timestamped record of customer privacy consents and revocation requests</p>
        </div>
      </div>

      <div className="space-y-3">
        {consents.map((c, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{c.contact}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">{c.type} • {c.date}</div>
            </div>
            <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${
              c.status === "Granted" ? "bg-emerald-950 text-emerald-400 border border-emerald-800" : "bg-red-950 text-red-400 border border-red-800"
            }`}>
              {c.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
