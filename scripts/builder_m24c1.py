import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    write_file("frontend/src/pages/auth/LoginPage.tsx", """import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { Zap, Lock, Mail, ArrowRight, ShieldCheck } from "lucide-react";
import { api } from "../../services/api";
import { useAuth } from "../../context/AuthContext";

export const LoginPage: React.FC = () => {
  const [email, setEmail] = useState("admin@clientflow.internal");
  const [password, setPassword] = useState("AdminSecret123!");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);
    try {
      const res = await api.login({ email, password });
      login(res.data);
      navigate("/dashboard");
    } catch (err: any) {
      setError(err.response?.data?.detail?.message || "Invalid credentials.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDemoLogin = async () => {
    setEmail("admin@clientflow.internal");
    setPassword("AdminSecret123!");
    setIsLoading(true);
    try {
      const res = await api.login({ email: "admin@clientflow.internal", password: "AdminSecret123!" });
      login(res.data);
      navigate("/dashboard");
    } catch (err) {
      try {
        await api.register({
          email: "admin@clientflow.internal",
          password: "AdminSecret123!",
          first_name: "Alexander",
          last_name: "Vance",
          organization_name: "Apex Global Dynamics"
        });
        const res = await api.login({ email: "admin@clientflow.internal", password: "AdminSecret123!" });
        login(res.data);
        navigate("/dashboard");
      } catch (regErr: any) {
        setError("Unable to authenticate demo user.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col justify-center py-12 sm:px-6 lg:px-8 relative overflow-hidden">
      <div className="sm:mx-auto sm:w-full sm:max-w-md relative z-10 text-center">
        <div className="w-12 h-12 rounded-2xl bg-emerald-500 text-slate-950 mx-auto flex items-center justify-center font-bold shadow-lg shadow-emerald-500/25 mb-4">
          <Zap className="w-7 h-7 fill-current" />
        </div>
        <h2 className="text-2xl font-bold tracking-tight text-white">ClientFlow CRM</h2>
        <p className="mt-1 text-xs text-slate-400">Enterprise High-Velocity CRM & Operations</p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md relative z-10 px-4">
        <div className="bg-slate-900/90 py-8 px-6 shadow-2xl rounded-2xl border border-slate-800">
          {error && <div className="mb-4 p-3 rounded-lg bg-rose-500/10 text-rose-400 text-xs">{error}</div>}
          <form className="space-y-4" onSubmit={handleSubmit}>
            <div>
              <label className="block text-xs font-medium text-slate-300">Corporate Email</label>
              <input type="email" required className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-xs text-white" value={email} onChange={e => setEmail(e.target.value)} />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-300">Password</label>
              <input type="password" required className="w-full bg-slate-800 border border-slate-700 rounded-lg p-2.5 text-xs text-white" value={password} onChange={e => setPassword(e.target.value)} />
            </div>
            <button type="submit" disabled={isLoading} className="w-full py-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold text-xs rounded-lg">
              {isLoading ? "Authenticating..." : "Sign In to Platform"}
            </button>
          </form>
          <div className="mt-4 pt-4 border-t border-slate-800">
            <button type="button" onClick={handleDemoLogin} className="w-full py-2 bg-slate-800 text-emerald-400 font-medium text-xs rounded-lg border border-slate-700">
              ⚡ Quick Demo 1-Click Login
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
""")

    write_file("frontend/src/pages/dashboard/DashboardPage.tsx", """import React, { useEffect, useState } from "react";
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
""")

    print("Part C1 generated.")

if __name__ == '__main__':
    run()
