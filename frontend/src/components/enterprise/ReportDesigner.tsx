import React, { useState } from "react";
import { BarChart3, PieChart, LineChart, Table, Download, RefreshCw } from "lucide-react";
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

const SAMPLE_CHART_DATA = [
  { month: "Jan", revenue: 145000, deals: 12 },
  { month: "Feb", revenue: 198000, deals: 16 },
  { month: "Mar", revenue: 240000, deals: 21 },
  { month: "Apr", revenue: 215000, deals: 18 },
  { month: "May", revenue: 280000, deals: 24 },
  { month: "Jun", revenue: 350000, deals: 29 }
];

export const ReportDesigner: React.FC = () => {
  const [metric, setMetric] = useState<"revenue" | "deals">("revenue");
  const [chartType, setChartType] = useState<"bar" | "line">("bar");

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-emerald-400" />
            Executive Report & Visual Analytics Studio
          </h3>
          <p className="text-xs text-slate-400">Configure customized cross-sectional telemetry and pipeline conversions</p>
        </div>
        <div className="flex items-center gap-3">
          <select
            value={metric}
            onChange={e => setMetric(e.target.value as any)}
            className="bg-slate-800 border border-slate-700 text-xs text-white rounded-lg px-3 py-1.5 focus:outline-none"
          >
            <option value="revenue">Closed Revenue ($)</option>
            <option value="deals">Deals Won (Count)</option>
          </select>
        </div>
      </div>

      <div className="h-64 bg-slate-950 p-4 rounded-xl border border-slate-800">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={SAMPLE_CHART_DATA}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis dataKey="month" stroke="#64748b" fontSize={11} />
            <YAxis stroke="#64748b" fontSize={11} tickFormatter={val => metric === "revenue" ? `$${val/1000}k` : val} />
            <Tooltip
              contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", borderRadius: "8px", fontSize: "11px" }}
              itemStyle={{ color: "#10b981" }}
            />
            <Bar dataKey={metric} fill="#10b981" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
