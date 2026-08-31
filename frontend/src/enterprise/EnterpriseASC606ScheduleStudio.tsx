import React, { useState } from "react";
import { Calculator, DollarSign, Calendar, CheckCircle2, FileText } from "lucide-react";

export const EnterpriseASC606ScheduleStudio: React.FC = () => {
  const schedules = [
    { period: "2026-09", rec: "$20,833.33", def: "$229,166.67", status: "Recognized" },
    { period: "2026-10", rec: "$20,833.33", def: "$208,333.34", status: "Scheduled" },
    { period: "2026-11", rec: "$20,833.33", def: "$187,500.01", status: "Scheduled" },
    { period: "2026-12", rec: "$20,833.33", def: "$166,666.68", status: "Scheduled" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Calculator className="w-5 h-5 text-emerald-400" />
            ASC 606 / IFRS 15 Revenue Amortization Schedule
          </h3>
          <p className="text-xs text-slate-400">Straight-line and multi-element revenue recognition engine for multi-year contracts</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          ASC 606 Compliant
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Total Contract Value</span>
          <div className="text-2xl font-bold text-white">$250,000.00</div>
          <span className="text-[10px] text-slate-400">12-Month Enterprise SaaS Term</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Monthly Amortization</span>
          <div className="text-2xl font-bold text-emerald-400">$20,833.33 / Mo</div>
          <span className="text-[10px] text-emerald-400">Straight-Line Over Time</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Ending Deferred Balance</span>
          <div className="text-2xl font-bold text-white">$229,166.67</div>
          <span className="text-[10px] text-slate-400">Auto-Balancing General Ledger</span>
        </div>
      </div>

      <div className="space-y-3">
        {schedules.map((s, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">Period: {s.period}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Recognized: <span className="text-emerald-400 font-bold">{s.rec}</span> • Ending Deferred: {s.def}</div>
            </div>
            <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${
              s.status === "Recognized" ? "bg-emerald-950 text-emerald-400 border border-emerald-800" : "bg-slate-800 text-slate-400"
            }`}>
              {s.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
