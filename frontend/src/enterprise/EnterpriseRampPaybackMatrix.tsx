import React, { useState } from "react";
import { TrendingUp, Users, DollarSign, Award, CheckCircle2 } from "lucide-react";

export const EnterpriseRampPaybackMatrix: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <DollarSign className="w-5 h-5 text-emerald-400" />
            Sales Rep Ramp Cost Payback & ROI Modeler
          </h3>
          <p className="text-xs text-slate-400">Calculate months required for ramped rep gross profit to amortize initial hiring and OTE draw</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          4.8 Mo Average Payback
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Ramp Investment per Rep</span>
          <div className="text-2xl font-bold text-white">$62,500</div>
          <span className="text-[10px] text-slate-400">3.5 Months Average Ramp</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Post-Ramp Monthly GP</span>
          <div className="text-2xl font-bold text-emerald-400">$13,000</div>
          <span className="text-[10px] text-emerald-400">Based on $85k Average Deal Size</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Payback Period</span>
          <div className="text-2xl font-bold text-emerald-400">4.8 Months</div>
          <span className="text-[10px] text-slate-400">Industry Benchmark: &lt; 9 Mo</span>
        </div>
      </div>
    </div>
  );
};
