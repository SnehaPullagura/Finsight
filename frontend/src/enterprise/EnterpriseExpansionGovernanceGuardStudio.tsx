import React, { useState } from "react";
import { ShieldCheck, AlertCircle, CheckCircle2, DollarSign } from "lucide-react";

export const EnterpriseExpansionGovernanceGuardStudio: React.FC = () => {
  const audits = [
    { account: "Wayne Enterprises", health: 94, tickets: 0, invoices: 0, status: "Clear to Propose" },
    { account: "Stark Industries", health: 88, tickets: 0, invoices: 0, status: "Clear to Propose" },
    { account: "Cyberdyne Systems", health: 62, tickets: 1, invoices: 0, status: "Blocked (Sev 1 Open)" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            Customer Expansion Governance & Prerequisite Guard
          </h3>
          <p className="text-xs text-slate-400">Automated policy checks preventing upsell outreach during open Sev-1 outages or billing disputes</p>
        </div>
      </div>

      <div className="space-y-3">
        {audits.map((a, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{a.account}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Health: {a.health} • Open Tickets: {a.tickets} • Overdue Invoices: {a.invoices}</div>
            </div>
            <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${
              a.status === "Clear to Propose" ? "bg-emerald-950 text-emerald-400 border border-emerald-800" : "bg-red-950 text-red-400 border border-red-800"
            }`}>
              {a.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
