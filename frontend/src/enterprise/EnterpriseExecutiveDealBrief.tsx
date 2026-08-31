import React, { useState } from "react";
import { FileText, Building, DollarSign, Users, Award, ShieldCheck, CheckCircle2 } from "lucide-react";

export const EnterpriseExecutiveDealBrief: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <FileText className="w-5 h-5 text-emerald-400" />
            Executive Deal Brief & Sign-Off Packet
          </h3>
          <p className="text-xs text-slate-400">Automated deal memorandum for CRO and Finance executive review</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Approved for Signature
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase">Opportunity</span>
          <div className="text-sm font-bold text-white">Stark Industries — Global License</div>
          <span className="text-xs text-emerald-400 font-semibold">$250,000 Total Value</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase">Pricing Guardrails</span>
          <div className="text-sm font-bold text-white">10% Volume Discount Applied</div>
          <span className="text-xs text-slate-400">Within Standard Margin Band</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase">MEDDIC Qualification</span>
          <div className="text-sm font-bold text-emerald-400">Score: 90 / 100</div>
          <span className="text-xs text-slate-400">Economic Buyer & Champion Confirmed</span>
        </div>
      </div>
    </div>
  );
};
