import React, { useEffect, useState } from "react";
import { DollarSign, TrendingUp, Users, Target, HeartHandshake, ArrowUpRight } from "lucide-react";
import { api } from "../../services/api";
import { DashboardMetrics } from "../../types";

export const DashboardPage: React.FC = () => {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);

  useEffect(() => {
    api.getDashboardAnalytics().then(res => setMetrics(res.data)).catch(console.error);
  }, []);

  if (!metrics) return <div className="p-8 text-center text-sm text-slate-500">Loading real-time executive analytics...</div>;

  const cards = [
    { label: "Total Pipeline Value", val: metrics.total_pipeline_value.formatted_value, change: "+14.2%", icon: <DollarSign className="w-5 h-5 text-emerald-600" /> },
    { label: "Weighted Forecast", val: metrics.weighted_forecast.formatted_value, change: "+8.5%", icon: <TrendingUp className="w-5 h-5 text-blue-600" /> },
    { label: "Deal Win Rate", val: metrics.win_rate.formatted_value, change: "+3.1%", icon: <Target className="w-5 h-5 text-purple-600" /> },
    { label: "Avg Customer Health", val: metrics.customer_avg_health.formatted_value, change: "+1.0%", icon: <HeartHandshake className="w-5 h-5 text-teal-600" /> },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-900">Executive CRM Intelligence</h1>
        <p className="text-xs text-slate-500">Real-time revenue telemetry and pipeline velocity metrics</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {cards.map((c, idx) => (
          <div key={idx} className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs">
            <div className="flex items-center justify-between">
              <div className="p-2 rounded-lg bg-slate-50">{c.icon}</div>
              <span className="text-xs font-semibold text-emerald-600">{c.change}</span>
            </div>
            <div className="mt-3">
              <div className="text-2xl font-bold text-slate-900">{c.val}</div>
              <div className="text-xs text-slate-500">{c.label}</div>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-2xs">
          <h3 className="text-sm font-bold text-slate-900 mb-4">Conversion Funnel</h3>
          <div className="space-y-3">
            {metrics.conversion_funnel.map((step, idx) => (
              <div key={idx} className="p-3 bg-slate-50 rounded-lg">
                <div className="flex justify-between text-xs font-semibold mb-1">
                  <span>{step.stage_name}</span>
                  <span>{step.count} Records ({step.conversion_rate_pct}%)</span>
                </div>
                <div className="w-full h-2 bg-slate-200 rounded-full overflow-hidden">
                  <div className="h-full bg-emerald-500 rounded-full" style={{ width: `${step.conversion_rate_pct}%` }}></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-2xs">
          <h3 className="text-sm font-bold text-slate-900 mb-4">Sales Rep Leaderboard</h3>
          <div className="divide-y divide-slate-100">
            {metrics.rep_leaderboard.map((rep, idx) => (
              <div key={idx} className="py-3 flex justify-between items-center">
                <div>
                  <div className="text-xs font-bold text-slate-800">{rep.user_name}</div>
                  <div className="text-[11px] text-slate-500">{rep.deals_won_count} Deals Won</div>
                </div>
                <div className="text-right">
                  <div className="text-xs font-bold text-slate-900">${rep.revenue_won.toLocaleString()}</div>
                  <div className="text-[10px] text-emerald-600 font-semibold">{rep.quota_attainment_pct}% attainment</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
