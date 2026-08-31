import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Wallet,
  ArrowLeftRight,
  PieChart,
  Target,
  CalendarCheck,
  TrendingUp,
  Activity,
  SlidersHorizontal,
  Bot,
  AlertTriangle,
  FileSpreadsheet,
  FileText,
  Shield,
  Layers
} from 'lucide-react';

const NAV_ITEMS = [
  { label: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
  { label: 'Financial Health', path: '/health', icon: Activity, badge: 'Core' },
  { label: 'Cash Flow Explorer', path: '/cashflow', icon: TrendingUp },
  { label: 'Scenario Simulator', path: '/scenarios', icon: SlidersHorizontal, badge: 'What-If' },
  { label: 'AI Assistant', path: '/assistant', icon: Bot, badge: 'RAG' },
  { label: 'Financial Accounts', path: '/accounts', icon: Wallet },
  { label: 'Transactions', path: '/transactions', icon: ArrowLeftRight },
  { label: 'Budgets & Discipline', path: '/budgets', icon: PieChart },
  { label: 'Financial Goals', path: '/goals', icon: Target },
  { label: 'Recurring & EMIs', path: '/recurring', icon: CalendarCheck },
  { label: 'Forecasts & Risk', path: '/forecasts', icon: Layers },
  { label: 'Analytics Hub', path: '/analytics', icon: PieChart },
  { label: 'Anomalies', path: '/anomalies', icon: AlertTriangle },
  { label: 'Data Import', path: '/imports', icon: FileSpreadsheet },
  { label: 'Financial Reports', path: '/reports', icon: FileText },
  { label: 'Admin & Registry', path: '/admin', icon: Shield }
];

export const Sidebar: React.FC = () => {
  return (
    <aside className="w-64 bg-slate-950 border-r border-slate-800 flex flex-col h-screen sticky top-0 shrink-0">
      {/* Brand Header */}
      <div className="h-16 px-6 flex items-center gap-3 border-b border-slate-800 bg-slate-900/30">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-500 via-indigo-600 to-violet-600 flex items-center justify-center text-white font-extrabold shadow-lg shadow-indigo-600/30">
          <Activity className="w-5 h-5 text-white" />
        </div>
        <div>
          <h1 className="font-extrabold text-base tracking-tight text-white flex items-center gap-1.5">
            FinSight <span className="text-[10px] px-1.5 py-0.5 rounded-md bg-indigo-600/30 text-indigo-400 font-mono font-bold border border-indigo-500/30">AI</span>
          </h1>
          <p className="text-[10px] text-slate-400 font-medium">Financial Intelligence</p>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 overflow-y-auto p-3 space-y-1">
        {NAV_ITEMS.map(item => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold transition group ${
                  isActive
                    ? 'bg-gradient-to-r from-indigo-600 to-indigo-700 text-white shadow-md shadow-indigo-600/20'
                    : 'text-slate-400 hover:text-slate-100 hover:bg-slate-900/70'
                }`
              }
            >
              <div className="flex items-center gap-3">
                <Icon className="w-4 h-4 transition group-hover:scale-110" />
                <span>{item.label}</span>
              </div>
              {item.badge && (
                <span className="text-[9px] px-1.5 py-0.5 rounded-full bg-slate-800/80 text-indigo-300 font-bold border border-indigo-500/20">
                  {item.badge}
                </span>
              )}
            </NavLink>
          );
        })}
      </nav>

      {/* Footer Pill */}
      <div className="p-4 border-t border-slate-900 bg-slate-950/80">
        <div className="p-3 rounded-xl bg-slate-900/70 border border-slate-800 text-[11px] text-slate-400 space-y-1">
          <p className="font-bold text-slate-200">FinSight Enterprise</p>
          <p className="text-[10px] text-slate-500">v1.0.0 • 3 ML Models Active</p>
        </div>
      </div>
    </aside>
  );
};
