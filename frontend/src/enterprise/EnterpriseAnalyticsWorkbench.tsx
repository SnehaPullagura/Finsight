import React, { useState } from "react";
import { BarChart3, LineChart, PieChart, Activity, DollarSign, Users, Award, TrendingUp } from "lucide-react";
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

const MONTHLY_REVENUE_TREND = [
  { month: "Jan", arr: 1200000, mrr: 100000, expansion: 15000, churn: 2000 },
  { month: "Feb", arr: 1350000, mrr: 112500, expansion: 18000, churn: 1500 },
  { month: "Mar", arr: 1520000, mrr: 126600, expansion: 22000, churn: 3000 },
  { month: "Apr", arr: 1780000, mrr: 148300, expansion: 29000, churn: 1000 },
  { month: "May", arr: 2100000, mrr: 175000, expansion: 35000, churn: 2500 },
  { month: "Jun", arr: 2450000, mrr: 204100, expansion: 42000, churn: 1800 }
];

export const EnterpriseAnalyticsWorkbench: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <span className="text-xs text-slate-400 font-medium uppercase tracking-wider">Annual Run Rate (ARR)</span>
          <div className="text-2xl font-bold text-white mt-1">$2,450,000</div>
          <div className="text-xs text-emerald-400 mt-2 font-medium">↑ +104.1% YoY Growth</div>
        </div>
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <span className="text-xs text-slate-400 font-medium uppercase tracking-wider">Net Revenue Retention (NRR)</span>
          <div className="text-2xl font-bold text-white mt-1">128.4%</div>
          <div className="text-xs text-emerald-400 mt-2 font-medium">Top Quartile SaaS Benchmark</div>
        </div>
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <span className="text-xs text-slate-400 font-medium uppercase tracking-wider">Gross Logo Retention</span>
          <div className="text-2xl font-bold text-white mt-1">97.2%</div>
          <div className="text-xs text-emerald-400 mt-2 font-medium">0.3% Churn per Quarter</div>
        </div>
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <span className="text-xs text-slate-400 font-medium uppercase tracking-wider">Sales Velocity Index</span>
          <div className="text-2xl font-bold text-white mt-1">42 Days</div>
          <div className="text-xs text-emerald-400 mt-2 font-medium">↓ -12 Days Faster Cycle</div>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl shadow-xl space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-emerald-400" />
              ARR Waterfall & Monthly Expansion Trajectory
            </h3>
            <p className="text-xs text-slate-400">Quarterly growth trajectory with new bookings, account expansions, and churn offsets</p>
          </div>
        </div>

        <div className="h-72 bg-slate-950 p-4 rounded-xl border border-slate-800">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={MONTHLY_REVENUE_TREND}>
              <defs>
                <linearGradient id="colorArr" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.4}/>
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="month" stroke="#64748b" fontSize={11} />
              <YAxis stroke="#64748b" fontSize={11} tickFormatter={val => `$${val/1000000}M`} />
              <Tooltip
                contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", borderRadius: "8px", fontSize: "11px" }}
              />
              <Area type="monotone" dataKey="arr" stroke="#10b981" fillOpacity={1} fill="url(#colorArr)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};
