import React, { useState } from "react";
import { Award, Zap, DollarSign, CheckCircle2 } from "lucide-react";

export const EnterpriseSPIFFIncentiveStudio: React.FC = () => {
  const spiffs = [
    { name: "Legacy Competitor Takeover Bounty", amount: "$3,000", criteria: "Rip-and-replace of Salesforce or Dynamics" },
    { name: "Multi-Year Enterprise Commitment Bonus", amount: "$2,500", criteria: "3+ Year upfront prepaid agreement" },
    { name: "AI Copilot Strategic Adoption Kicker", amount: "$1,000", criteria: "Attaching AI Assistant to any >50 seat deal" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Zap className="w-5 h-5 text-amber-400" />
            Strategic Sales SPIFFs & Deal Acceleration Bounties
          </h3>
          <p className="text-xs text-slate-400">Real-time performance kickers rewarding multi-year commitments and competitive takeovers</p>
        </div>
      </div>

      <div className="space-y-3">
        {spiffs.map((s, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{s.name}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">{s.criteria}</div>
            </div>
            <div className="text-right">
              <span className="text-sm font-bold text-emerald-400">{s.amount} Cash Bonus</span>
              <span className="text-[10px] text-slate-500 block">Instant Payroll Add</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
