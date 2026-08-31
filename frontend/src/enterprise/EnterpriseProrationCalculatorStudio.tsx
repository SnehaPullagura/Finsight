import React, { useState } from "react";
import { Calculator, DollarSign, Calendar, CheckCircle2 } from "lucide-react";

export const EnterpriseProrationCalculatorStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Calculator className="w-5 h-5 text-emerald-400" />
            Mid-Cycle License Upgrade & Proration Engine
          </h3>
          <p className="text-xs text-slate-400">Day-level exact proration credits for seat additions co-termed to monthly/annual billing dates</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Co-Termed Exact
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Additional Seats Added</span>
          <div className="text-2xl font-bold text-white">+10 Seats</div>
          <span className="text-[10px] text-slate-400">18 Days Remaining in Month</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Prorated Amount Due</span>
          <div className="text-2xl font-bold text-emerald-400">$600.00</div>
          <span className="text-[10px] text-emerald-400">Immediate Invoice Item</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Next Full Cycle Charge</span>
          <div className="text-2xl font-bold text-white">$1,000.00 / Mo</div>
          <span className="text-[10px] text-slate-400">Normal Monthly Renewal</span>
        </div>
      </div>
    </div>
  );
};
