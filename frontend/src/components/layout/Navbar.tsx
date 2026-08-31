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
