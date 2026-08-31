import React, { useState, useEffect } from 'react';
import { api } from '../../services/api';
import { Shield, Cpu, Activity, Database, CheckCircle2 } from 'lucide-react';

export const AdminPage: React.FC = () => {
  const [metrics, setMetrics] = useState<any>(null);

  useEffect(() => {
    api.getAdminMetrics().then(setMetrics).catch(() => {});
  }, []);

  return (
    <div className="space-y-6">
      <div className="pb-3 border-b border-slate-800">
        <h1 className="text-2xl font-black text-white tracking-tight">Platform Admin & Model Registry</h1>
        <p className="text-xs text-slate-400 mt-1">Live model governance, drift monitoring, and platform operational metrics.</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="glass-panel rounded-2xl p-5 border border-slate-800">
          <p className="text-xs text-slate-400 font-semibold uppercase">Total Users</p>
          <p className="text-2xl font-black text-white mono mt-1">{metrics?.total_users || 1}</p>
        </div>
        <div className="glass-panel rounded-2xl p-5 border border-slate-800">
          <p className="text-xs text-slate-400 font-semibold uppercase">Transactions Managed</p>
          <p className="text-2xl font-black text-white mono mt-1">{metrics?.total_transactions_managed || 0}</p>
        </div>
        <div className="glass-panel rounded-2xl p-5 border border-slate-800">
          <p className="text-xs text-slate-400 font-semibold uppercase">Accounts Connected</p>
          <p className="text-2xl font-black text-white mono mt-1">{metrics?.total_accounts_connected || 0}</p>
        </div>
        <div className="glass-panel rounded-2xl p-5 border border-slate-800">
          <p className="text-xs text-slate-400 font-semibold uppercase">Total Volume</p>
          <p className="text-2xl font-black text-emerald-400 mono mt-1">₹{metrics?.total_volume_processed?.toLocaleString('en-IN') || 0}</p>
        </div>
      </div>

      {/* Model Registry List */}
      <div className="glass-panel rounded-3xl p-6 border border-slate-800 space-y-4">
        <div className="flex items-center gap-2 pb-3 border-b border-slate-800">
          <Cpu className="w-5 h-5 text-indigo-400" />
          <h3 className="font-extrabold text-sm text-slate-200 uppercase tracking-wider">Active ML Model Registry (Exactly 3 Core Models)</h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {metrics?.active_ml_models?.map((m: any) => (
            <div key={m.id} className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-bold text-xs text-white">{m.model_name.replace('_', ' ').toUpperCase()}</span>
                <span className="text-[9px] font-bold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">Active</span>
              </div>
              <p className="text-[11px] text-slate-400">{m.algorithm}</p>
              <div className="flex justify-between text-xs pt-2 border-t border-slate-800/60">
                <span className="text-slate-500">Accuracy / Score:</span>
                <span className="mono font-bold text-indigo-400">{(m.accuracy_or_metric * 100).toFixed(1)}%</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-slate-500">Samples:</span>
                <span className="mono text-slate-300">{m.training_sample_count?.toLocaleString()}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
