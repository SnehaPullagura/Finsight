import React, { useState } from "react";
import { Globe, TrendingUp, DollarSign, Target, Award } from "lucide-react";

export const EnterpriseTAMExpansionStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Globe className="w-5 h-5 text-emerald-400" />
            Total Addressable Market (TAM) Expansion Modeler
          </h3>
          <p className="text-xs text-slate-400">Market sizing, serviceable obtainable market (SOM), and expansion horizons</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Total Addressable Market (TAM)</span>
          <div className="text-2xl font-bold text-white">$14.5 Billion</div>
          <span className="text-[10px] text-slate-400">120,000 Global Enterprise Accounts</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Serviceable Market (SAM)</span>
          <div className="text-2xl font-bold text-emerald-400">$3.2 Billion</div>
          <span className="text-[10px] text-emerald-400">Tier 1 Target Tech / Finance Verticals</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Obtainable Target (SOM)</span>
          <div className="text-2xl font-bold text-purple-400">$450 Million</div>
          <span className="text-[10px] text-purple-400">3-Year Strategic Runway Target</span>
        </div>
      </div>
    </div>
  );
};
