import React, { useState } from "react";
import { FileText, DollarSign, CheckCircle2, Award, Plus } from "lucide-react";

export const EnterpriseExpansionDealBuilderStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <FileText className="w-5 h-5 text-emerald-400" />
            1-Click Co-Termed Expansion Quote Generator
          </h3>
          <p className="text-xs text-slate-400">Instantly generate co-termed expansion proposals with automated volume discount tiers</p>
        </div>
        <button className="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-500 text-white px-3 py-1.5 rounded-lg text-xs font-semibold shadow transition-colors">
          <Plus className="w-4 h-4" />
          Generate Quote PDF
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Additional Quoted Seats</span>
          <div className="text-2xl font-bold text-white">+15 Enterprise Seats</div>
          <span className="text-[10px] text-slate-400">$1,200 / Seat / Year</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Volume Discount Applied</span>
          <div className="text-2xl font-bold text-emerald-400">10% ($1,800 Off)</div>
          <span className="text-[10px] text-emerald-400">Pre-Approved CPQ Guardrail</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Net Contract Value</span>
          <div className="text-2xl font-bold text-emerald-400">$16,200 ARR</div>
          <span className="text-[10px] text-slate-400">Co-Termed to Master Agreement</span>
        </div>
      </div>
    </div>
  );
};
