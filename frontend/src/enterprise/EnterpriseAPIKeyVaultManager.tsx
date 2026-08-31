import React, { useState } from "react";
import { Key, Shield, Plus, CheckCircle2, Lock } from "lucide-react";

export const EnterpriseAPIKeyVaultManager: React.FC = () => {
  const keys = [
    { name: "Production Stripe Webhook Receiver", key: "cfk_prod_8a9...3f12", created: "2026-08-15", scopes: "billing.read, invoices.write" },
    { name: "CI/CD Deployment & Ingestion Pipeline", key: "cfk_pipe_1b2...99ee", created: "2026-08-20", scopes: "contacts.write, deals.write" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Key className="w-5 h-5 text-emerald-400" />
            API Key Vault & Scoped Access Tokens
          </h3>
          <p className="text-xs text-slate-400">Cryptographically hashed API access tokens with fine-grained endpoint permissions</p>
        </div>
        <button className="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-500 text-white px-3 py-1.5 rounded-lg text-xs font-semibold shadow transition-colors">
          <Plus className="w-4 h-4" />
          Generate Key
        </button>
      </div>

      <div className="space-y-3">
        {keys.map((k, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{k.name}</div>
              <div className="text-[11px] font-mono text-slate-400 mt-0.5">{k.key}</div>
              <div className="text-[10px] text-slate-500 mt-1">Scopes: {k.scopes}</div>
            </div>
            <span className="text-xs text-emerald-400 font-semibold flex items-center gap-1">
              <CheckCircle2 className="w-3.5 h-3.5" /> Active
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
