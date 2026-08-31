import React, { useState, useEffect } from 'react';
import { api } from '../../services/api';
import { Wallet, Plus, RefreshCw, CheckCircle, ShieldCheck, ArrowUpRight } from 'lucide-react';
import { FinancialAccount } from '../../types';

export const AccountsPage: React.FC = () => {
  const [accounts, setAccounts] = useState<FinancialAccount[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [name, setName] = useState('');
  const [type, setType] = useState('bank');
  const [balance, setBalance] = useState(50000);
  const [institution, setInstitution] = useState('HDFC Bank');
  const [reconcileId, setReconcileId] = useState<number | null>(null);
  const [actualBalance, setActualBalance] = useState(0);

  const loadAccounts = () => {
    api.getAccounts().then(setAccounts).catch(() => {});
  };

  useEffect(() => {
    loadAccounts();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    await api.createAccount({
      name,
      account_type: type,
      current_balance: Number(balance),
      institution_name: institution,
      is_primary: accounts.length === 0
    });
    setShowModal(false);
    loadAccounts();
  };

  const handleReconcile = async (id: number) => {
    await api.reconcileAccount(id, { actual_balance: Number(actualBalance) });
    setReconcileId(null);
    loadAccounts();
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-white tracking-tight">Financial Accounts</h1>
          <p className="text-xs text-slate-400 mt-1">Manage connected bank accounts, cards, loans, and investment portfolios.</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold flex items-center gap-2 transition"
        >
          <Plus className="w-4 h-4" /> Add Account
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {accounts.map(acc => (
          <div key={acc.id} className="glass-panel rounded-3xl p-5 border border-slate-800 space-y-4 relative overflow-hidden">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-2xl bg-slate-800/80 border border-slate-700/60 flex items-center justify-center text-indigo-400">
                  <Wallet className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-bold text-sm text-white">{acc.name}</h3>
                  <p className="text-[11px] text-slate-500">{acc.institution_name} • {acc.account_number_masked}</p>
                </div>
              </div>
              {acc.is_primary && (
                <span className="text-[9px] font-bold px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">Primary</span>
              )}
            </div>

            <div className="space-y-1">
              <span className="text-[10px] text-slate-500 uppercase tracking-wider font-semibold">Available Balance</span>
              <div className="text-2xl font-black text-white mono tracking-tight">
                ₹{acc.current_balance?.toLocaleString('en-IN')}
              </div>
            </div>

            <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
              <span className="text-slate-500 capitalize">{acc.account_type.replace('_', ' ')}</span>
              <button
                onClick={() => { setReconcileId(acc.id); setActualBalance(acc.current_balance); }}
                className="text-indigo-400 hover:underline flex items-center gap-1 font-semibold"
              >
                <RefreshCw className="w-3 h-3" /> Reconcile
              </button>
            </div>

            {reconcileId === acc.id && (
              <div className="p-3 rounded-2xl bg-slate-900 border border-slate-700 space-y-2 mt-2">
                <label className="text-[11px] font-bold text-slate-300 block">Actual Statement Balance (₹)</label>
                <input
                  type="number"
                  value={actualBalance}
                  onChange={e => setActualBalance(Number(e.target.value))}
                  className="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-1.5 text-xs text-white"
                />
                <div className="flex justify-end gap-2 pt-1">
                  <button onClick={() => setReconcileId(null)} className="px-3 py-1 rounded-lg bg-slate-800 text-[11px] text-slate-400">Cancel</button>
                  <button onClick={() => handleReconcile(acc.id)} className="px-3 py-1 rounded-lg bg-indigo-600 text-[11px] font-bold text-white">Save</button>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="glass-panel rounded-3xl p-6 border border-slate-800 w-full max-w-md space-y-4">
            <h3 className="font-extrabold text-base text-white">Add Financial Account</h3>
            <form onSubmit={handleCreate} className="space-y-3 text-xs">
              <div>
                <label className="block text-slate-300 font-bold mb-1">Account Nickname</label>
                <input type="text" value={name} onChange={e => setName(e.target.value)} required className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white" placeholder="e.g. HDFC Salary" />
              </div>
              <div>
                <label className="block text-slate-300 font-bold mb-1">Institution</label>
                <input type="text" value={institution} onChange={e => setInstitution(e.target.value)} className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white" />
              </div>
              <div>
                <label className="block text-slate-300 font-bold mb-1">Account Type</label>
                <select value={type} onChange={e => setType(e.target.value)} className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white">
                  <option value="bank">Bank Checking / Salary</option>
                  <option value="savings">Savings Account</option>
                  <option value="credit_card">Credit Card</option>
                  <option value="investment">Investment Portfolio</option>
                  <option value="loan">Loan Account</option>
                  <option value="cash">Cash Wallet</option>
                </select>
              </div>
              <div>
                <label className="block text-slate-300 font-bold mb-1">Initial Balance (₹)</label>
                <input type="number" value={balance} onChange={e => setBalance(Number(e.target.value))} className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white" />
              </div>
              <div className="flex justify-end gap-2 pt-2">
                <button type="button" onClick={() => setShowModal(false)} className="px-4 py-2 rounded-xl bg-slate-800 text-slate-300">Cancel</button>
                <button type="submit" className="px-5 py-2 rounded-xl bg-indigo-600 text-white font-bold">Create Account</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
