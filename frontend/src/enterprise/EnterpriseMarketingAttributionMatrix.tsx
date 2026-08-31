import React, { useState } from "react";
import { Award, TrendingUp, Filter, ArrowUpRight, DollarSign } from "lucide-react";

export const EnterpriseMarketingAttributionMatrix: React.FC = () => {
  const channels = [
    { channel: "Direct Executive Outreach", cost: 15000, revenue: 320000, roas: "21.3x", leads: 42, wonDeals: 12 },
    { channel: "Google Search (High-Intent B2B)", cost: 25000, revenue: 410000, roas: "16.4x", leads: 180, wonDeals: 18 },
    { channel: "LinkedIn Sponsored Content", cost: 18000, revenue: 195000, roas: "10.8x", leads: 95, wonDeals: 8 },
    { channel: "Product Demonstration Webinars", cost: 8000, revenue: 160000, roas: "20.0x", leads: 64, wonDeals: 7 }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-emerald-400" />
            Marketing Campaign ROI & Multi-Channel Performance
          </h3>
          <p className="text-xs text-slate-400">Return on Ad Spend (ROAS) and direct pipeline conversion attribution across marketing channels</p>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-xs text-left">
          <thead className="bg-slate-950 text-slate-400 font-semibold border-b border-slate-800">
            <tr>
              <th className="p-3">Campaign Channel</th>
              <th className="p-3 text-right">Spend</th>
              <th className="p-3 text-right">Leads</th>
              <th className="p-3 text-right">Won Deals</th>
              <th className="p-3 text-right text-emerald-400">Revenue Attributed</th>
              <th className="p-3 text-right">ROAS</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-white">
            {channels.map((ch, idx) => (
              <tr key={idx} className="hover:bg-slate-800/30">
                <td className="p-3 font-medium">{ch.channel}</td>
                <td className="p-3 text-right text-slate-400">${ch.cost.toLocaleString()}</td>
                <td className="p-3 text-right">{ch.leads}</td>
                <td className="p-3 text-right">{ch.wonDeals}</td>
                <td className="p-3 text-right font-bold text-emerald-400">${ch.revenue.toLocaleString()}</td>
                <td className="p-3 text-right font-bold text-purple-400">{ch.roas}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
