import React, { useState } from "react";
import { Users, TrendingUp, Filter, CheckCircle2, DollarSign } from "lucide-react";

export const EnterpriseCohortRetentionStudio: React.FC = () => {
  const cohorts = [
    { month: "Jan 2026", size: 45, m0: "100%", m1: "98%", m2: "96%", m3: "95%", m4: "94%", m5: "94%" },
    { month: "Feb 2026", size: 52, m0: "100%", m1: "97%", m2: "95%", m3: "95%", m4: "93%", m5: "-" },
    { month: "Mar 2026", size: 60, m0: "100%", m1: "99%", m2: "97%", m3: "96%", m4: "-", m5: "-" },
    { month: "Apr 2026", size: 75, m0: "100%", m1: "98%", m2: "96%", m3: "-", m4: "-", m5: "-" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Users className="w-5 h-5 text-emerald-400" />
            Customer & Revenue Cohort Retention Matrix
          </h3>
          <p className="text-xs text-slate-400">Monthly Net Revenue Retention (NRR) heatmap across customer acquisition cohorts</p>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-xs text-left">
          <thead className="bg-slate-950 text-slate-400 font-semibold border-b border-slate-800">
            <tr>
              <th className="p-3">Cohort</th>
              <th className="p-3 text-right">Accounts</th>
              <th className="p-3 text-center">Month 0</th>
              <th className="p-3 text-center">Month 1</th>
              <th className="p-3 text-center">Month 2</th>
              <th className="p-3 text-center">Month 3</th>
              <th className="p-3 text-center">Month 4</th>
              <th className="p-3 text-center">Month 5</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-white">
            {cohorts.map((c, idx) => (
              <tr key={idx} className="hover:bg-slate-800/30">
                <td className="p-3 font-semibold">{c.month}</td>
                <td className="p-3 text-right text-slate-400">{c.size}</td>
                <td className="p-3 text-center font-bold text-emerald-400">{c.m0}</td>
                <td className="p-3 text-center text-emerald-400">{c.m1}</td>
                <td className="p-3 text-center text-emerald-400">{c.m2}</td>
                <td className="p-3 text-center text-emerald-400">{c.m3}</td>
                <td className="p-3 text-center text-emerald-400">{c.m4}</td>
                <td className="p-3 text-center text-emerald-400">{c.m5}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
