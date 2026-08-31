import React, { useState } from "react";
import { Target, CheckCircle2, ShieldCheck, Award } from "lucide-react";

export const EnterpriseBayesianWinRateStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Target className="w-5 h-5 text-emerald-400" />
            Bayesian Calibrated Deal Win Rate Estimator
          </h3>
          <p className="text-xs text-slate-400">Continuous Bayesian posterior updating based on champion validation and budget verification</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          88.4% Posterior Win Rate
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Base Stage Probability</span>
          <div className="text-2xl font-bold text-white">60.0% Prior</div>
          <span className="text-[10px] text-slate-400">Proposal Stage Benchmark</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Likelihood Multiplier</span>
          <div className="text-2xl font-bold text-emerald-400">2.45x Ratio</div>
          <span className="text-[10px] text-emerald-400">Champion + InfoSec Verified</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Calibrated Posterior</span>
          <div className="text-2xl font-bold text-emerald-400">88.4% Prob</div>
          <span className="text-[10px] text-slate-400">High Confidence Close</span>
        </div>
      </div>
    </div>
  );
};
