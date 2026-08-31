import React, { useState } from "react";
import { TrendingUp, Activity, PieChart, Users, DollarSign, Layers } from "lucide-react";
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

const TELEMETRY_DATA = [
  { day: "Mon", active_users: 120, api_calls: 45000, pipeline_added: 80000 },
  { day: "Tue", active_users: 145, api_calls: 52000, pipeline_added: 120000 },
  { day: "Wed", active_users: 160, api_calls: 61000, pipeline_added: 95000 },
  { day: "Thu", active_users: 180, api_calls: 78000, pipeline_added: 210000 },
  { day: "Fri", active_users: 195, api_calls: 84000, pipeline_added: 340000 },
  { day: "Sat", active_users: 85, api_calls: 31000, pipeline_added: 45000 },
  { day: "Sun", active_users: 70, api_calls: 28000, pipeline_added: 20000 }
];

export const DataAnalyticsStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Activity className="w-5 h-5 text-emerald-400" />
            Platform Telemetry & Operational Analytics
          </h3>
          <p className="text-xs text-slate-400">High-velocity telemetry across pipeline creation, API usage, and user activity</p>
        </div>
      </div>

      <div className="h-64 bg-slate-950 p-4 rounded-xl border border-slate-800">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={TELEMETRY_DATA}>
            <defs>
              <linearGradient id="colorPipeline" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#10b981" stopOpacity={0.4}/>
                <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis dataKey="day" stroke="#64748b" fontSize={11} />
            <YAxis stroke="#64748b" fontSize={11} tickFormatter={val => `$${val/1000}k`} />
            <Tooltip
              contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", borderRadius: "8px", fontSize: "11px" }}
              itemStyle={{ color: "#10b981" }}
            />
            <Area type="monotone" dataKey="pipeline_added" stroke="#10b981" fillOpacity={1} fill="url(#colorPipeline)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
