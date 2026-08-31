import React, { useState } from "react";
import { Shield, Search, Filter, Lock, CheckCircle2, AlertTriangle, ArrowRight } from "lucide-react";

interface AuditEntry {
  id: string;
  timestamp: string;
  actor: string;
  action: string;
  entity: string;
  blockHash: string;
  isVerified: boolean;
}

const AUDIT_DATA: AuditEntry[] = [
  { id: "blk-891", timestamp: "2026-09-01 02:15:30", actor: "alex.vance@initech.internal", action: "DEAL_STAGE_ADVANCE", entity: "Deal #4582", blockHash: "7a8b...3f91", isVerified: true },
  { id: "blk-890", timestamp: "2026-09-01 01:42:10", actor: "sarah.connor@stark.internal", action: "DISCOUNT_APPROVED", entity: "Quote #1092", blockHash: "e4c1...99a0", isVerified: true },
  { id: "blk-889", timestamp: "2026-09-01 00:18:45", actor: "system.event_bus", action: "SLA_ESCALATION_DISPATCH", entity: "Ticket #831", blockHash: "2b5f...77d3", isVerified: true },
  { id: "blk-888", timestamp: "2026-08-31 23:55:12", actor: "bruce.wayne@wayne.internal", action: "CONTRACT_EXECUTED", entity: "Contract #224", blockHash: "9a01...12ff", isVerified: true }
];

export const EnterpriseAuditLedgerViewer: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Shield className="w-5 h-5 text-emerald-400" />
            Immutable SOC2 Cryptographic Audit Ledger
          </h3>
          <p className="text-xs text-slate-400">Append-only blockchain verified audit blocks with SHA-256 state signatures</p>
        </div>
        <span className="flex items-center gap-1.5 bg-emerald-950 border border-emerald-800 text-emerald-400 px-3 py-1 rounded-full text-xs font-semibold">
          <CheckCircle2 className="w-3.5 h-3.5" />
          Chain Verified (100% Integrity)
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-xs text-left">
          <thead className="bg-slate-950 text-slate-400 font-semibold border-b border-slate-800">
            <tr>
              <th className="p-3">Block Hash</th>
              <th className="p-3">Timestamp (UTC)</th>
              <th className="p-3">Actor Email</th>
              <th className="p-3">Action Type</th>
              <th className="p-3">Target Entity</th>
              <th className="p-3 text-right">Verification</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-white">
            {AUDIT_DATA.map(entry => (
              <tr key={entry.id} className="hover:bg-slate-800/30">
                <td className="p-3 font-mono text-slate-400">{entry.blockHash}</td>
                <td className="p-3 text-slate-300">{entry.timestamp}</td>
                <td className="p-3 font-medium">{entry.actor}</td>
                <td className="p-3"><span className="bg-slate-800 px-2 py-0.5 rounded text-[11px] font-mono text-emerald-400">{entry.action}</span></td>
                <td className="p-3 text-slate-300">{entry.entity}</td>
                <td className="p-3 text-right">
                  <span className="text-emerald-400 font-medium flex items-center justify-end gap-1">
                    <CheckCircle2 className="w-3 h-3" /> Valid
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
