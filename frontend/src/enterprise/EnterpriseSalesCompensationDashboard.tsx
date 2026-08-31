import React, { useState } from "react";
import { Award, TrendingUp, DollarSign, Target, CheckCircle2, ChevronRight } from "lucide-react";

export const EnterpriseSalesCompensationDashboard: React.FC = () => {
  const reps = [
    { name: "Alex Vance", quota: 250000, closed: 340000, attainment: "136.0%", commission: 42500, tier: "Tier 3 (2.0x)" },
    { name: "Sarah Connor", quota: 300000, closed: 315000, attainment: "105.0%", commission: 32250, tier: "Tier 2 (1.5x)" },
    { name: "John Wick", quota: 200000, closed: 180000, attainment: "90.0%", commission: 18000, tier: "Tier 1 (1.0x)" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Award className="w-5 h-5 text-emerald-400" />
            Sales Compensation & Commission Waterfall Dashboard
          </h3>
          <p className="text-xs text-slate-400">Real-time quota attainment tracking with automated multi-tier accelerator calculation</p>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-xs text-left">
          <thead className="bg-slate-950 text-slate-400 font-semibold border-b border-slate-800">
            <tr>
              <th className="p-3">Sales Representative</th>
              <th className="p-3 text-right">Quota Target</th>
              <th className="p-3 text-right">Closed Revenue</th>
              <th className="p-3 text-right">Attainment %</th>
              <th className="p-3">Active Accelerator</th>
              <th className="p-3 text-right text-emerald-400 font-bold">Commission Payout</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-white">
            {reps.map((r, idx) => (
              <tr key={idx} className="hover:bg-slate-800/30">
                <td className="p-3 font-semibold">{r.name}</td>
                <td className="p-3 text-right text-slate-400">${r.quota.toLocaleString()}</td>
                <td className="p-3 text-right font-medium">${r.closed.toLocaleString()}</td>
                <td className="p-3 text-right text-emerald-400 font-bold">{r.attainment}</td>
                <td className="p-3"><span className="bg-slate-800 text-purple-300 px-2 py-0.5 rounded text-[11px] font-mono">{r.tier}</span></td>
                <td className="p-3 text-right font-bold text-emerald-400">${r.commission.toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
