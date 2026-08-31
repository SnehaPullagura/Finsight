import React, { useState, useEffect } from 'react';
import { api } from '../../services/api';
import { StatCard } from '../../components/ui/StatCard';
import { HealthScoreGauge } from '../../components/ui/HealthScoreGauge';
import {
  Wallet, TrendingUp, TrendingDown, ArrowUpRight, ArrowDownRight,
  Sparkles, SlidersHorizontal, AlertTriangle, CheckCircle2, ChevronRight
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { FinancialHealth, CashFlowSummary, Transaction, FinancialAccount } from '../../types';

export const DashboardPage: React.FC = () => {
  const [health, setHealth] = useState<FinancialHealth | null>(null);
  const [cashflow, setCashflow] = useState<CashFlowSummary | null>(null);
  const [accounts, setAccounts] = useState<FinancialAccount[]>([]);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      api.getHealthScore(),
      api.getCashFlowSummary(),
      api.getAccounts(),
      api.getTransactions('?limit=8')
    ]).then(([h, c, a, t]) => {
      setHealth(h);
      setCashflow(c);
      setAccounts(a);
      setTransactions(t);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  const totalLiquid = accounts
    .filter(a => ['bank', 'savings', 'cash'].includes(a.account_type))
    .reduce((sum, a) => sum + a.current_balance, 0);

  return (
    <div className="space-y-6">
      {/* Top Banner / Key Differentiation Callout */}
      <div className="rounded-3xl bg-gradient-to-r from-indigo-900/60 via-indigo-950/80 to-slate-950 border border-indigo-500/20 p-6 md:p-8 flex flex-col md:flex-row items-start md:items-center justify-between gap-6 relative overflow-hidden">
        <div className="space-y-2 z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-bold border border-indigo-500/30">
            <Sparkles className="w-3.5 h-3.5" /> Decision-Support Intelligence
          </div>
          <h2 className="text-2xl md:text-3xl font-extrabold text-white tracking-tight">
            Financial Health & Future Cash-Flow Clarity
          </h2>
          <p className="text-sm text-slate-300 max-w-2xl leading-relaxed">
            FinSight continuously scores your financial stability across 6 pillars, predicts shortage risks, and lets you test what-if scenarios in real-time.
          </p>
        </div>
        <div className="flex items-center gap-3 shrink-0 z-10">
          <Link
            to="/scenarios"
            className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 text-white text-xs font-extrabold hover:from-indigo-500 hover:to-violet-500 shadow-lg shadow-indigo-600/30 flex items-center gap-2 transition"
          >
            <SlidersHorizontal className="w-4 h-4" /> Simulate Scenario
          </Link>
          <Link
            to="/assistant"
            className="px-5 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-slate-200 text-xs font-bold hover:bg-slate-800 transition"
          >
            Ask AI Assistant
          </Link>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Total Liquid Balance"
          value={`₹${totalLiquid.toLocaleString('en-IN')}`}
          subtitle={`${accounts.length} Active Accounts`}
          icon={Wallet}
        />
        <StatCard
          title="30-Day Cash In"
          value={`₹${(cashflow?.total_cash_in || 0).toLocaleString('en-IN')}`}
          trend="+12% MoM"
          trendUp={true}
          icon={ArrowDownRight}
        />
        <StatCard
          title="30-Day Cash Out"
          value={`₹${(cashflow?.total_cash_out || 0).toLocaleString('en-IN')}`}
          subtitle={`₹${(cashflow?.average_daily_burn_rate || 0).toFixed(0)}/day burn`}
          icon={ArrowUpRight}
        />
        <StatCard
          title="Net Cash Flow"
          value={`${(cashflow?.net_cash_flow || 0) >= 0 ? '+' : ''}₹${(cashflow?.net_cash_flow || 0).toLocaleString('en-IN')}`}
          trend={`${cashflow?.savings_rate_percent || 0}% Saved`}
          trendUp={(cashflow?.net_cash_flow || 0) >= 0}
          icon={TrendingUp}
        />
      </div>

      {/* Health Score & 6 Pillars Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Gauge Card */}
        <div className="glass-panel rounded-3xl p-6 border border-slate-800 flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <h3 className="font-extrabold text-sm text-slate-200 uppercase tracking-wider">Financial Health Score</h3>
            <Link to="/health" className="text-xs text-indigo-400 font-bold hover:underline flex items-center gap-1">
              Full Breakdown <ChevronRight className="w-3.5 h-3.5" />
            </Link>
          </div>
          <HealthScoreGauge score={health?.overall_score || 0} grade={health?.grade || 'Calculating...'} />
          <p className="text-xs text-slate-400 text-center leading-relaxed mt-2">
            {health?.explanation || 'Analyzing transactions, debt burden, and savings rates...'}
          </p>
        </div>

        {/* 6 Pillars Breakdown */}
        <div className="lg:col-span-2 glass-panel rounded-3xl p-6 border border-slate-800 space-y-4">
          <div className="flex items-center justify-between pb-2 border-b border-slate-800">
            <h3 className="font-extrabold text-sm text-slate-200 uppercase tracking-wider">6 Pillar Health Decomposition</h3>
            <span className="text-xs text-slate-500 font-medium">Proprietary Mathematical Model</span>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {health?.pillars.map(p => (
              <div key={p.pillar_name} className="p-3.5 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-300">{p.pillar_name}</span>
                  <span className={`text-xs font-black mono px-2 py-0.5 rounded-full ${p.score >= 75 ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'}`}>
                    {p.score}/100
                  </span>
                </div>
                <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-indigo-500 to-violet-500 rounded-full transition-all duration-700"
                    style={{ width: `${p.score}%` }}
                  />
                </div>
                <div className="flex justify-between text-[11px] text-slate-500">
                  <span>{p.metric_value}</span>
                  <span className="capitalize">{p.status}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Cash Flow Timeline & Recent Transactions */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Cash Flow Timeline */}
        <div className="lg:col-span-2 glass-panel rounded-3xl p-6 border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-extrabold text-sm text-slate-200 uppercase tracking-wider">Cash-Flow Trajectory (Net In vs Out)</h3>
              <p className="text-xs text-slate-500 mt-0.5">30-day liquidity runway: <span className="text-indigo-400 font-bold">{cashflow?.liquidity_runway_days || 0} days</span></p>
            </div>
            <Link to="/cashflow" className="text-xs text-indigo-400 font-bold hover:underline">Explore Flow →</Link>
          </div>
          
          <div className="space-y-2">
            {cashflow?.daily_timeline.slice(-7).map(pt => (
              <div key={pt.date} className="flex items-center justify-between p-3 rounded-xl bg-slate-900/40 border border-slate-800/80 hover:border-slate-700 text-xs">
                <span className="mono font-semibold text-slate-400">{pt.date}</span>
                <div className="flex items-center gap-4">
                  <span className="text-emerald-400 mono font-bold">+₹{pt.cash_in.toLocaleString('en-IN')}</span>
                  <span className="text-rose-400 mono font-bold">-₹{pt.cash_out.toLocaleString('en-IN')}</span>
                  <span className="text-white mono font-extrabold w-24 text-right">₹{pt.projected_balance.toLocaleString('en-IN')}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Transactions Feed */}
        <div className="glass-panel rounded-3xl p-6 border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="font-extrabold text-sm text-slate-200 uppercase tracking-wider">Recent Activity</h3>
            <Link to="/transactions" className="text-xs text-indigo-400 font-bold hover:underline">View All</Link>
          </div>
          <div className="space-y-2.5">
            {transactions.slice(0, 5).map(tx => (
              <div key={tx.id} className="p-3 rounded-2xl bg-slate-900/60 border border-slate-800/80 flex items-center justify-between text-xs">
                <div className="min-w-0 pr-2">
                  <p className="font-bold text-slate-200 truncate">{tx.description}</p>
                  <p className="text-[10px] text-slate-500 mt-0.5">{tx.merchant_name || 'Direct'} • {tx.transaction_date}</p>
                </div>
                <span className={`font-mono font-extrabold shrink-0 ${tx.transaction_type === 'income' ? 'text-emerald-400' : 'text-slate-200'}`}>
                  {tx.transaction_type === 'income' ? '+' : '-'}₹{tx.amount.toLocaleString('en-IN')}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
