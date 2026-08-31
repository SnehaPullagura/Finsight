import React, { useState } from "react";
import { Clock, TrendingUp, BarChart3 } from "lucide-react";

export const EnterpriseStageDurationMatrix: React.FC = () => {
  const durations = [
    { stage: "Discovery Call", avg: "4.2d", median: "3.5d", min: "1d", max: "12d" },
    { stage: "Technical Scoping", avg: "8.5d", median: "7.0d", min: "3d", max: "21d" },
    { stage: "CPQ Quote Generation", avg: "5.1d", median: "4.0d", min: "1d", max: "14d" },
    { stage: "Executive Negotiation", avg: "14.8d", median: "12.0d", min: "5d", max: "45d" },
    { stage: "Legal & Procurement", avg: "12.0d", median: "10.0d", min: "4d", max: "30d" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Clock className="w-5 h-5 text-emerald-400" />
            Stage Duration Distribution & Sales Pacing
          </h3>
          <p className="text-xs text-slate-400">Average, median, and maximum days spent by opportunities across pipeline stages</p>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-xs text-left">
          <thead className="bg-slate-950 text-slate-400 font-semibold border-b border-slate-800">
            <tr>
              <th className="p-3">Sales Pipeline Stage</th>
              <th className="p-3 text-right">Average Days</th>
              <th className="p-3 text-right">Median Days</th>
              <th className="p-3 text-right">Min Days</th>
              <th className="p-3 text-right">Max Days</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-white">
            {durations.map((d, idx) => (
              <tr key={idx} className="hover:bg-slate-800/30">
                <td className="p-3 font-semibold">{d.stage}</td>
                <td className="p-3 text-right font-bold text-emerald-400">{d.avg}</td>
                <td className="p-3 text-right text-slate-300">{d.median}</td>
                <td className="p-3 text-right text-slate-500">{d.min}</td>
                <td className="p-3 text-right text-amber-400">{d.max}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
