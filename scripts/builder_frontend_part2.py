import os
from scripts.common import write_file

def build_frontend_components():
    print("Building UI components, Layout and Core Pages...")

    # Layout Components
    write_file("frontend/src/components/layout/Navbar.tsx", """
import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { Bell, Shield, User as UserIcon, LogOut, Search, Activity } from 'lucide-react';
import { api } from '../../services/api';
import { NotificationItem } from '../../types';

export const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const [notifications, setNotifications] = useState<NotificationItem[]>([]);
  const [showNotifs, setShowNotifs] = useState(false);

  useEffect(() => {
    if (user) {
      api.getNotifications().then(setNotifications).catch(() => {});
    }
  }, [user]);

  const unreadCount = notifications.filter(n => !n.is_read).length;

  return (
    <header className="h-16 border-b border-slate-800 bg-slate-900/80 backdrop-blur px-6 flex items-center justify-between sticky top-0 z-30">
      <div className="flex items-center gap-4 flex-1 max-w-md">
        <div className="relative w-full">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search transactions, accounts, merchants..."
            className="w-full bg-slate-950/60 border border-slate-800 rounded-xl pl-9 pr-4 py-2 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition"
          />
        </div>
      </div>

      <div className="flex items-center gap-4">
        {/* Live System Status Pill */}
        <div className="hidden md:flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>Engine Active</span>
        </div>

        {/* Notifications Dropdown */}
        <div className="relative">
          <button
            onClick={() => setShowNotifs(!showNotifs)}
            className="p-2 rounded-xl bg-slate-800/80 hover:bg-slate-800 text-slate-300 hover:text-white transition relative"
          >
            <Bell className="w-4 h-4" />
            {unreadCount > 0 && (
              <span className="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-rose-500 text-white text-[10px] font-bold flex items-center justify-center">
                {unreadCount}
              </span>
            )}
          </button>

          {showNotifs && (
            <div className="absolute right-0 mt-2 w-80 rounded-2xl glass-dropdown shadow-2xl p-4 z-50 animate-in fade-in slide-in-from-top-2">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-2">
                <h4 className="font-bold text-xs text-slate-200">Notifications ({unreadCount})</h4>
                <button
                  onClick={() => api.markAllNotificationsRead().then(() => setNotifications(n => n.map(x => ({...x, is_read: true}))))}
                  className="text-[10px] text-indigo-400 hover:underline"
                >
                  Mark all read
                </button>
              </div>
              <div className="space-y-2 max-h-60 overflow-y-auto pr-1">
                {notifications.length === 0 ? (
                  <p className="text-xs text-slate-500 py-4 text-center">No new notifications</p>
                ) : (
                  notifications.map(n => (
                    <div key={n.id} className={`p-2.5 rounded-xl text-xs ${n.is_read ? 'bg-slate-900/40 text-slate-400' : 'bg-indigo-950/40 border border-indigo-500/20 text-slate-200'}`}>
                      <p className="font-semibold text-white">{n.title}</p>
                      <p className="text-[11px] text-slate-400 mt-0.5 leading-snug">{n.message}</p>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}
        </div>

        {/* User Profile */}
        <div className="flex items-center gap-3 pl-2 border-l border-slate-800">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-600 flex items-center justify-center font-bold text-xs text-white shadow-lg shadow-indigo-500/20">
            {user?.full_name?.charAt(0) || 'U'}
          </div>
          <div className="hidden lg:block text-left">
            <p className="text-xs font-bold text-slate-200 leading-tight">{user?.full_name || 'Guest User'}</p>
            <p className="text-[10px] text-slate-400">{user?.preferred_currency || 'INR'} • {user?.role || 'user'}</p>
          </div>
          <button
            onClick={logout}
            title="Logout"
            className="p-2 rounded-xl text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 transition"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>
  );
};
""")

    write_file("frontend/src/components/layout/Sidebar.tsx", """
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
""")

    write_file("frontend/src/components/layout/AppLayout.tsx", """
import React from 'react';
import { Outlet } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { Navbar } from './Navbar';

export const AppLayout: React.FC = () => {
  return (
    <div className="flex min-h-screen bg-[#030712] text-slate-100">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <Navbar />
        <main className="flex-1 p-6 md:p-8 overflow-y-auto max-w-7xl mx-auto w-full">
          <Outlet />
        </main>
      </div>
    </div>
  );
};
""")

    # UI Widgets
    write_file("frontend/src/components/ui/StatCard.tsx", """
import React from 'react';
import { LucideIcon } from 'lucide-react';

interface StatCardProps {
  title: string;
  value: string;
  subtitle?: string;
  icon: LucideIcon;
  trend?: string;
  trendUp?: boolean;
  color?: string;
}

export const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  subtitle,
  icon: Icon,
  trend,
  trendUp,
  color = 'indigo'
}) => {
  return (
    <div className="glass-panel rounded-2xl p-5 border border-slate-800 shadow-lg hover:border-slate-700 transition">
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{title}</span>
        <div className="w-9 h-9 rounded-xl bg-slate-800/80 border border-slate-700/60 flex items-center justify-center text-indigo-400">
          <Icon className="w-4 h-4" />
        </div>
      </div>
      <div className="text-2xl font-black text-white tracking-tight mono">{value}</div>
      {(subtitle || trend) && (
        <div className="flex items-center gap-2 mt-2 text-xs">
          {trend && (
            <span className={`font-bold px-1.5 py-0.5 rounded ${trendUp ? 'bg-emerald-500/10 text-emerald-400' : 'bg-rose-500/10 text-rose-400'}`}>
              {trend}
            </span>
          )}
          {subtitle && <span className="text-slate-500">{subtitle}</span>}
        </div>
      )}
    </div>
  );
};
""")

    write_file("frontend/src/components/ui/HealthScoreGauge.tsx", """
import React from 'react';

interface HealthScoreGaugeProps {
  score: number;
  grade: string;
}

export const HealthScoreGauge: React.FC<HealthScoreGaugeProps> = ({ score, grade }) => {
  const circumference = 2 * Math.PI * 42;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  const getColor = () => {
    if (score >= 80) return '#10B981'; // Emerald
    if (score >= 65) return '#6366F1'; // Indigo
    if (score >= 50) return '#F59E0B'; // Amber
    return '#EF4444'; // Rose
  };

  return (
    <div className="flex flex-col items-center justify-center p-4">
      <div className="relative w-36 h-36 flex items-center justify-center">
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
          {/* Background circle */}
          <circle
            cx="50"
            cy="50"
            r="42"
            stroke="currentColor"
            strokeWidth="10"
            className="text-slate-800"
            fill="transparent"
          />
          {/* Progress circle */}
          <circle
            cx="50"
            cy="50"
            r="42"
            stroke={getColor()}
            strokeWidth="10"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        <div className="absolute flex flex-col items-center justify-center text-center">
          <span className="text-3xl font-extrabold text-white mono leading-none">{score}</span>
          <span className="text-[10px] text-slate-400 font-semibold uppercase tracking-widest mt-1">/ 100</span>
        </div>
      </div>
      <div className="mt-3 px-3 py-1 rounded-full bg-slate-800 text-xs font-extrabold text-white border border-slate-700">
        {grade}
      </div>
    </div>
  );
};
""")

    print("Phase 7 components part 2 created!")

if __name__ == "__main__":
    build_frontend_components()
