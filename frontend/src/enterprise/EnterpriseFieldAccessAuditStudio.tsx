import React, { useState } from "react";
import { ShieldCheck, Eye, Lock, CheckCircle2 } from "lucide-react";

export const EnterpriseFieldAccessAuditStudio: React.FC = () => {
  const events = [
    { user: "admin@clientflow.internal", table: "companies", fields: "tax_id, bank_routing", ip: "10.0.4.12", time: "2026-08-30 18:22:10" },
    { user: "billing_mgr@clientflow.internal", table: "invoices", fields: "stripe_customer_id", ip: "10.0.4.18", time: "2026-08-30 17:45:04" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Eye className="w-5 h-5 text-emerald-400" />
            Field-Level Decryption Access Audit Trail
          </h3>
          <p className="text-xs text-slate-400">SOC 2 & HIPAA continuous logging of all encrypted field decryption reads</p>
        </div>
      </div>

      <div className="space-y-3">
        {events.map((e, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{e.user} accessed {e.table}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Fields: {e.fields} • IP: {e.ip}</div>
            </div>
            <span className="text-[10px] text-slate-500">{e.time}</span>
          </div>
        ))}
      </div>
    </div>
  );
};
