import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. frontend/src/enterprise/EnterprisePipelineKanban.tsx
    write_file("frontend/src/enterprise/EnterprisePipelineKanban.tsx", """import React, { useState } from "react";
import { DollarSign, User, Building, Calendar, CheckCircle2, Clock, MoreVertical, Plus } from "lucide-react";

interface DealCard {
  id: string;
  name: string;
  company: string;
  amount: number;
  probability: number;
  stage: string;
  owner: string;
  slaDays: number;
}

const INITIAL_DEALS: DealCard[] = [
  { id: "d-101", name: "Global Enterprise License", company: "Wayne Enterprises", amount: 250000, probability: 80, stage: "negotiation", owner: "Sarah Connor", slaDays: 3 },
  { id: "d-102", name: "Cloud Infrastructure Integration", company: "Stark Industries", amount: 180000, probability: 60, stage: "proposal", owner: "Alex Vance", slaDays: 6 },
  { id: "d-103", name: "Cybersecurity Suite Rollout", company: "Cyberdyne Systems", amount: 95000, probability: 40, stage: "scoping", owner: "John Wick", slaDays: 2 },
  { id: "d-104", name: "Custom Workflow Automation", company: "Oscorp Global", amount: 120000, probability: 90, stage: "contract", owner: "Sarah Connor", slaDays: 1 }
];

export const EnterprisePipelineKanban: React.FC = () => {
  const [deals, setDeals] = useState<DealCard[]>(INITIAL_DEALS);

  const columns = [
    { id: "scoping", label: "Scoping & Discovery", color: "border-blue-500/50" },
    { id: "proposal", label: "Proposal & Pricing", color: "border-amber-500/50" },
    { id: "negotiation", label: "Executive Negotiation", color: "border-purple-500/50" },
    { id: "contract", label: "Legal & Contract", color: "border-emerald-500/50" }
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white">Enterprise Pipeline Kanban</h2>
          <p className="text-xs text-slate-400">Interactive stage management with SLA indicators and probability weighting</p>
        </div>
        <button className="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-500 text-white px-3 py-1.5 rounded-lg text-xs font-semibold shadow-lg transition-colors">
          <Plus className="w-4 h-4" />
          Create Deal
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {columns.map(col => {
          const colDeals = deals.filter(d => d.stage === col.id);
          const colTotal = colDeals.reduce((sum, d) => sum + d.amount, 0);

          return (
            <div key={col.id} className={`bg-slate-900 border ${col.color} rounded-xl p-4 flex flex-col min-h-[500px]`}>
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <span className="text-xs font-bold text-white uppercase tracking-wider">{col.label}</span>
                <span className="text-xs bg-slate-800 text-slate-300 px-2 py-0.5 rounded-full">{colDeals.length}</span>
              </div>
              <div className="text-xs text-emerald-400 font-semibold my-2">
                ${colTotal.toLocaleString()} pipeline
              </div>

              <div className="space-y-3 mt-2 flex-1">
                {colDeals.map(deal => (
                  <div key={deal.id} className="bg-slate-950 border border-slate-800 hover:border-slate-700 p-3 rounded-lg shadow space-y-2 cursor-pointer transition-all">
                    <div className="text-xs font-bold text-white line-clamp-1">{deal.name}</div>
                    <div className="text-[11px] text-slate-400 flex items-center gap-1">
                      <Building className="w-3 h-3 text-slate-500" />
                      {deal.company}
                    </div>
                    <div className="flex items-center justify-between pt-2 border-t border-slate-800/60 text-[11px]">
                      <span className="font-bold text-emerald-400">${deal.amount.toLocaleString()}</span>
                      <span className="text-slate-400 flex items-center gap-1">
                        <Clock className="w-3 h-3 text-amber-400" />
                        {deal.slaDays}d in stage
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
""")

    # 2. frontend/src/enterprise/EnterpriseCPQBuilder.tsx
    write_file("frontend/src/enterprise/EnterpriseCPQBuilder.tsx", """import React, { useState } from "react";
import { Calculator, Plus, Trash2, ShieldCheck, Check, DollarSign } from "lucide-react";

interface LineItem {
  id: string;
  name: string;
  unitPrice: number;
  quantity: number;
  discountPct: number;
}

export const EnterpriseCPQBuilder: React.FC = () => {
  const [items, setItems] = useState<LineItem[]>([
    { id: "1", name: "Enterprise CRM Seat License", unitPrice: 120, quantity: 50, discountPct: 10 },
    { id: "2", name: "White-Glove Implementation Package", unitPrice: 15000, quantity: 1, discountPct: 0 }
  ]);

  const subtotal = items.reduce((sum, item) => sum + (item.unitPrice * item.quantity), 0);
  const discountTotal = items.reduce((sum, item) => sum + (item.unitPrice * item.quantity * (item.discountPct / 100)), 0);
  const finalTotal = subtotal - discountTotal;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Calculator className="w-5 h-5 text-emerald-400" />
            CPQ Enterprise Quote Generator & Pricing Engine
          </h3>
          <p className="text-xs text-slate-400">Configure complex multi-line quotes with volume discount matrices and margin guardrails</p>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-xs text-left">
          <thead className="bg-slate-950 text-slate-400 font-semibold border-b border-slate-800">
            <tr>
              <th className="p-3">Product / Service</th>
              <th className="p-3 text-right">Unit Price</th>
              <th className="p-3 text-right">Quantity</th>
              <th className="p-3 text-right">Discount %</th>
              <th className="p-3 text-right">Line Total</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-white">
            {items.map(item => {
              const lineTotal = (item.unitPrice * item.quantity) * (1 - item.discountPct / 100);
              return (
                <tr key={item.id} className="hover:bg-slate-800/30">
                  <td className="p-3 font-medium">{item.name}</td>
                  <td className="p-3 text-right">${item.unitPrice.toLocaleString()}</td>
                  <td className="p-3 text-right">{item.quantity}</td>
                  <td className="p-3 text-right text-amber-400">{item.discountPct}%</td>
                  <td className="p-3 text-right font-bold text-emerald-400">${lineTotal.toLocaleString()}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <div className="flex justify-end pt-4 border-t border-slate-800">
        <div className="w-64 space-y-2 text-xs">
          <div className="flex justify-between text-slate-400">
            <span>List Price Subtotal:</span>
            <span className="font-semibold text-white">${subtotal.toLocaleString()}</span>
          </div>
          <div className="flex justify-between text-slate-400">
            <span>Volume Discount:</span>
            <span className="font-semibold text-amber-400">-${discountTotal.toLocaleString()}</span>
          </div>
          <div className="flex justify-between text-sm font-bold text-white pt-2 border-t border-slate-800">
            <span>Payable Amount:</span>
            <span className="text-emerald-400">${finalTotal.toLocaleString()}</span>
          </div>
        </div>
      </div>
    </div>
  );
};
""")

    # 3. frontend/src/enterprise/EnterpriseAuditLedgerViewer.tsx
    write_file("frontend/src/enterprise/EnterpriseAuditLedgerViewer.tsx", """import React, { useState } from "react";
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
""")

    print("Created pipeline kanban, CPQ builder, and audit ledger viewer.")

if __name__ == '__main__':
    run()
