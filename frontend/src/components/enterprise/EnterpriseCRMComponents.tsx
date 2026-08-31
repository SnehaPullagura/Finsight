import React, { useState } from "react";
import { Shield, Sparkles, Filter, Database, CheckSquare, Search, Award } from "lucide-react";

export const MultiTouchAttributionView: React.FC = () => {
  const touchpoints = [
    { channel: "Google Search (Organic)", first_touch: 40, last_touch: 10, linear: 25, w_shaped: 30 },
    { channel: "LinkedIn Sponsored Ad", first_touch: 20, last_touch: 15, linear: 20, w_shaped: 25 },
    { channel: "Product Demo Webinar", first_touch: 10, last_touch: 35, linear: 30, w_shaped: 30 },
    { channel: "Direct Executive Outreach", first_touch: 30, last_touch: 40, linear: 25, w_shaped: 15 }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div>
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <Award className="w-5 h-5 text-emerald-400" />
          Multi-Touch Marketing Attribution Comparison
        </h3>
        <p className="text-xs text-slate-400">Compare pipeline revenue attribution across First Touch, Last Touch, Linear, and W-Shaped models</p>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-xs text-left">
          <thead className="bg-slate-950 text-slate-400 font-semibold border-b border-slate-800">
            <tr>
              <th className="p-3">Marketing Channel</th>
              <th className="p-3 text-right">First Touch %</th>
              <th className="p-3 text-right">Last Touch %</th>
              <th className="p-3 text-right">Linear %</th>
              <th className="p-3 text-right text-emerald-400 font-bold">W-Shaped %</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {touchpoints.map((tp, idx) => (
              <tr key={idx} className="hover:bg-slate-800/30 text-white">
                <td className="p-3 font-medium">{tp.channel}</td>
                <td className="p-3 text-right">{tp.first_touch}%</td>
                <td className="p-3 text-right">{tp.last_touch}%</td>
                <td className="p-3 text-right">{tp.linear}%</td>
                <td className="p-3 text-right text-emerald-400 font-bold">{tp.w_shaped}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
