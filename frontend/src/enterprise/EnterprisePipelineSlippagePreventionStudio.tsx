import React, { useState } from "react";
import { ShieldAlert, TrendingDown, CheckCircle2, DollarSign, Play } from "lucide-react";

export const EnterprisePipelineSlippagePreventionStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-amber-400" />
            Deal Slippage Auto-Remediation Playbook
          </h3>
          <p className="text-xs text-slate-400">Automated intervention blueprints triggered when enterprise deal velocity stagnates</p>
        </div>
        <button className="flex items-center gap-2 bg-amber-600 hover:bg-amber-500 text-white px-3 py-1.5 rounded-lg text-xs font-semibold shadow transition-colors">
          <Play className="w-4 h-4" />
          Deploy Intervention
        </button>
      </div>

      <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold text-white">Target Opportunity: Wayne Enterprises Global MSA ($250,000)</span>
          <span className="text-xs text-amber-400 font-semibold">Risk: 78 / 100</span>
        </div>
        <div className="space-y-2 text-xs text-slate-300">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>Schedule immediate CRO-to-CEO peer negotiation sync</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>Offer customized payment schedule ramp</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>Dispatch technical solutions engineer for immediate security review sign-off</span>
          </div>
        </div>
      </div>
    </div>
  );
};
