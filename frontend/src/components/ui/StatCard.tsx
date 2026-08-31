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
