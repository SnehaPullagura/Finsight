import React, { useState } from "react";
import { Globe, Users, Target, CheckCircle2, RefreshCw } from "lucide-react";

export const EnterpriseTerritoryOptimizerStudio: React.FC = () => {
  const territories = [
    { id: "TERR-1", name: "US West - Enterprise", accounts: 42, tam: "$8.4M", variance: "+2.1%", rep: "Alex Vance" },
    { id: "TERR-2", name: "US East - Financial Services", accounts: 38, tam: "$8.2M", variance: "-0.5%", rep: "Sarah Connor" },
    { id: "TERR-3", name: "EMEA & Strategic Accounts", accounts: 35, tam: "$8.6M", variance: "+4.2%", rep: "John Wick" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Globe className="w-5 h-5 text-emerald-400" />
            Enterprise Territory Optimizer & TAM Workload Equalizer
          </h3>
          <p className="text-xs text-slate-400">Algorithmic territory balancing ensuring equitable quota capacity across sales teams</p>
        </div>
        <button className="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-500 text-white px-3 py-1.5 rounded-lg text-xs font-semibold shadow transition-colors">
          <RefreshCw className="w-4 h-4" />
          Rebalance Territories
        </button>
      </div>

      <div className="space-y-3">
        {territories.map((t, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{t.name} ({t.id})</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Assigned Rep: {t.rep} • {t.accounts} Accounts • Total TAM: <span className="text-emerald-400 font-bold">{t.tam}</span></div>
            </div>
            <div className="text-right">
              <span className="text-xs font-bold text-emerald-400">{t.variance} Variance</span>
              <span className="text-[10px] text-slate-500 block">Balanced Territory</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
