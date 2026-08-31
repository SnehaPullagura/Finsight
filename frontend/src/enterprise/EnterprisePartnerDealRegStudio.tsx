import React, { useState } from "react";
import { Handshake, Award, ShieldCheck, CheckCircle2, DollarSign } from "lucide-react";

export const EnterprisePartnerDealRegStudio: React.FC = () => {
  const registrations = [
    { partner: "Accenture Digital", account: "Stark Industries", deal: "$450,000", margin: "15%", status: "Exclusivity Approved (90d)" },
    { partner: "Deloitte Consulting", account: "Wayne Enterprises", deal: "$280,000", margin: "15%", status: "Exclusivity Approved (90d)" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Handshake className="w-5 h-5 text-emerald-400" />
            Global SI & Co-Sell Deal Registration Portal
          </h3>
          <p className="text-xs text-slate-400">Automated conflict collision checks and 90-day lead exclusivity protection</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Portal Active
        </span>
      </div>

      <div className="space-y-3">
        {registrations.map((r, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{r.partner} → {r.account}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Registered Value: {r.deal} • Partner Incentive Margin: <span className="text-emerald-400 font-bold">{r.margin}</span></div>
            </div>
            <span className="text-xs font-semibold bg-emerald-950 text-emerald-400 border border-emerald-800 px-2.5 py-1 rounded-full">
              {r.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
