import os
from scripts.common import write_file

def build_remaining_pages():
    print("Building remaining dedicated frontend pages...")

    # 1. Accounts Page
    write_file("frontend/src/pages/accounts/AccountsPage.tsx", """
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
""")

    # 2. Transactions Page
    write_file("frontend/src/pages/transactions/TransactionsPage.tsx", """
import React, { useState, useEffect } from 'react';
import { api } from '../../services/api';
import { ArrowLeftRight, Plus, Search, Filter, Trash2, Tag, CheckCircle2 } from 'lucide-react';
import { Transaction, FinancialAccount, Category } from '../../types';

export const TransactionsPage: React.FC = () => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [accounts, setAccounts] = useState<FinancialAccount[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);
  
  // New transaction form
  const [desc, setDesc] = useState('');
  const [amt, setAmt] = useState(1500);
  const [txType, setTxType] = useState('expense');
  const [accId, setAccId] = useState<number>(0);
  const [catId, setCatId] = useState<number>(0);

  const loadData = () => {
    api.getTransactions().then(setTransactions).catch(() => {});
    api.getAccounts().then(a => { setAccounts(a); if (a.length > 0) setAccId(a[0].id); }).catch(() => {});
    api.getCategories().then(c => { setCategories(c); if (c.length > 0) setCatId(c[0].id); }).catch(() => {});
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    await api.createTransaction({
      account_id: Number(accId),
      category_id: Number(catId),
      amount: Number(amt),
      transaction_type: txType,
      transaction_date: new Date().toISOString().split('T')[0],
      description: desc
    });
    setShowModal(false);
    setDesc('');
    loadData();
  };

  const handleDelete = async (id: number) => {
    await api.deleteTransaction(id);
    loadData();
  };

  const filtered = transactions.filter(t =>
    t.description.toLowerCase().includes(search.toLowerCase()) ||
    t.merchant_name?.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-white tracking-tight">Transaction Intelligence</h1>
          <p className="text-xs text-slate-400 mt-1">Unified ledger with real-time NLP auto-categorization and confidence scoring.</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold flex items-center gap-2 transition"
        >
          <Plus className="w-4 h-4" /> Record Transaction
        </button>
      </div>

      {/* Filter Bar */}
      <div className="flex items-center gap-3">
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="Search by description or merchant..."
            className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-9 pr-4 py-2.5 text-xs text-white focus:outline-none focus:border-indigo-500"
          />
        </div>
      </div>

      {/* Table */}
      <div className="glass-panel rounded-3xl border border-slate-800 overflow-hidden shadow-xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-900/80 border-b border-slate-800 text-slate-400 uppercase font-semibold">
              <tr>
                <th className="px-6 py-3.5">Date</th>
                <th className="px-6 py-3.5">Description & Merchant</th>
                <th className="px-6 py-3.5">Category</th>
                <th className="px-6 py-3.5">Type</th>
                <th className="px-6 py-3.5 text-right">Amount</th>
                <th className="px-6 py-3.5 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {filtered.map(t => (
                <tr key={t.id} className="hover:bg-slate-900/40 transition">
                  <td className="px-6 py-4 mono text-slate-400 whitespace-nowrap">{t.transaction_date}</td>
                  <td className="px-6 py-4">
                    <p className="font-bold text-white">{t.description}</p>
                    {t.merchant_name && <p className="text-[10px] text-indigo-400 font-semibold">{t.merchant_name}</p>}
                  </td>
                  <td className="px-6 py-4">
                    <span className="px-2.5 py-1 rounded-full bg-slate-800 text-slate-300 text-[11px] font-medium border border-slate-700">
                      {t.category?.name || 'General'}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <span className={`capitalize font-bold ${t.transaction_type === 'income' ? 'text-emerald-400' : 'text-slate-300'}`}>
                      {t.transaction_type}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right mono font-extrabold text-white text-sm whitespace-nowrap">
                    {t.transaction_type === 'income' ? '+' : '-'}₹{t.amount?.toLocaleString('en-IN')}
                  </td>
                  <td className="px-6 py-4 text-right">
                    <button
                      onClick={() => handleDelete(t.id)}
                      className="p-1.5 rounded-lg text-slate-500 hover:text-rose-400 hover:bg-rose-500/10 transition"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="glass-panel rounded-3xl p-6 border border-slate-800 w-full max-w-md space-y-4">
            <h3 className="font-extrabold text-base text-white">Record Transaction</h3>
            <form onSubmit={handleCreate} className="space-y-3 text-xs">
              <div>
                <label className="block text-slate-300 font-bold mb-1">Description</label>
                <input type="text" value={desc} onChange={e => setDesc(e.target.value)} required className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white" placeholder="e.g. Starbucks Indiranagar" />
              </div>
              <div>
                <label className="block text-slate-300 font-bold mb-1">Amount (₹)</label>
                <input type="number" value={amt} onChange={e => setAmt(Number(e.target.value))} required className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white" />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-slate-300 font-bold mb-1">Type</label>
                  <select value={txType} onChange={e => setTxType(e.target.value)} className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white">
                    <option value="expense">Expense</option>
                    <option value="income">Income</option>
                    <option value="transfer">Transfer</option>
                  </select>
                </div>
                <div>
                  <label className="block text-slate-300 font-bold mb-1">Account</label>
                  <select value={accId} onChange={e => setAccId(Number(e.target.value))} className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white">
                    {accounts.map(a => <option key={a.id} value={a.id}>{a.name}</option>)}
                  </select>
                </div>
              </div>
              <div>
                <label className="block text-slate-300 font-bold mb-1">Category</label>
                <select value={catId} onChange={e => setCatId(Number(e.target.value))} className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white">
                  {categories.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
                </select>
              </div>
              <div className="flex justify-end gap-2 pt-2">
                <button type="button" onClick={() => setShowModal(false)} className="px-4 py-2 rounded-xl bg-slate-800 text-slate-300">Cancel</button>
                <button type="submit" className="px-5 py-2 rounded-xl bg-indigo-600 text-white font-bold">Save Transaction</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
""")

    # 3. Budgets Page
    write_file("frontend/src/pages/budgets/BudgetsPage.tsx", """
import React, { useState, useEffect } from 'react';
import { api } from '../../services/api';
import { PieChart, Plus, AlertCircle, CheckCircle2 } from 'lucide-react';
import { BudgetProgress, Category } from '../../types';

export const BudgetsPage: React.FC = () => {
  const [budgets, setBudgets] = useState<BudgetProgress[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [name, setName] = useState('');
  const [catId, setCatId] = useState<number>(0);
  const [amount, setAmount] = useState(15000);

  const loadData = () => {
    api.getBudgets().then(setBudgets).catch(() => {});
    api.getCategories().then(c => { setCategories(c); if (c.length > 0) setCatId(c[0].id); }).catch(() => {});
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    await api.createBudget({
      name,
      category_id: Number(catId),
      allocated_amount: Number(amount),
      start_date: new Date().toISOString().split('T')[0]
    });
    setShowModal(false);
    setName('');
    loadData();
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-white tracking-tight">Budgets & Discipline</h1>
          <p className="text-xs text-slate-400 mt-1">Real-time category burn rates, progress alerts, and 50/30/20 recommendations.</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold flex items-center gap-2 transition"
        >
          <Plus className="w-4 h-4" /> Create Budget
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {budgets.map(b => (
          <div key={b.id} className="glass-panel rounded-3xl p-6 border border-slate-800 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="font-bold text-sm text-white">{b.name}</h3>
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${b.status === 'good' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : b.status === 'warning' ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20' : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'}`}>
                {b.percentage_used}% used
              </span>
            </div>

            <div className="w-full h-2.5 bg-slate-800 rounded-full overflow-hidden">
              <div
                className={`h-full rounded-full transition-all duration-500 ${b.is_overbudget ? 'bg-rose-500' : b.percentage_used >= 80 ? 'bg-amber-500' : 'bg-indigo-500'}`}
                style={{ width: `${Math.min(100, b.percentage_used)}%` }}
              />
            </div>

            <div className="flex justify-between text-xs pt-1">
              <div>
                <p className="text-[10px] text-slate-500 font-semibold uppercase">Spent</p>
                <p className="font-bold text-white mono mt-0.5">₹{b.spent_amount.toLocaleString('en-IN')}</p>
              </div>
              <div className="text-right">
                <p className="text-[10px] text-slate-500 font-semibold uppercase">Limit</p>
                <p className="font-bold text-slate-300 mono mt-0.5">₹{b.allocated_amount.toLocaleString('en-IN')}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="glass-panel rounded-3xl p-6 border border-slate-800 w-full max-w-md space-y-4">
            <h3 className="font-extrabold text-base text-white">Create Category Budget</h3>
            <form onSubmit={handleCreate} className="space-y-3 text-xs">
              <div>
                <label className="block text-slate-300 font-bold mb-1">Budget Title</label>
                <input type="text" value={name} onChange={e => setName(e.target.value)} required className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white" placeholder="e.g. Monthly Dining Out" />
              </div>
              <div>
                <label className="block text-slate-300 font-bold mb-1">Category</label>
                <select value={catId} onChange={e => setCatId(Number(e.target.value))} className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white">
                  {categories.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-slate-300 font-bold mb-1">Monthly Spending Limit (₹)</label>
                <input type="number" value={amount} onChange={e => setAmount(Number(e.target.value))} required className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white" />
              </div>
              <div className="flex justify-end gap-2 pt-2">
                <button type="button" onClick={() => setShowModal(false)} className="px-4 py-2 rounded-xl bg-slate-800 text-slate-300">Cancel</button>
                <button type="submit" className="px-5 py-2 rounded-xl bg-indigo-600 text-white font-bold">Create Budget</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
""")

    # 4. Goals Page
    write_file("frontend/src/pages/goals/GoalsPage.tsx", """
import React, { useState, useEffect } from 'react';
import { api } from '../../services/api';
import { Target, Plus, TrendingUp, CheckCircle2 } from 'lucide-react';
import { FinancialGoal } from '../../types';

export const GoalsPage: React.FC = () => {
  const [goals, setGoals] = useState<FinancialGoal[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [name, setName] = useState('');
  const [targetAmt, setTargetAmt] = useState(200000);
  const [currentAmt, setCurrentAmt] = useState(50000);
  const [monthlyContrib, setMonthlyContrib] = useState(15000);

  const loadGoals = () => {
    api.getGoals().then(setGoals).catch(() => {});
  };

  useEffect(() => {
    loadGoals();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    const targetDate = new Date();
    targetDate.setMonth(targetDate.getMonth() + 12);
    await api.createGoal({
      name,
      target_amount: Number(targetAmt),
      current_amount: Number(currentAmt),
      monthly_contribution: Number(monthlyContrib),
      target_date: targetDate.toISOString().split('T')[0]
    });
    setShowModal(false);
    setName('');
    loadGoals();
  };

  const handleContribute = async (id: number) => {
    await api.contributeGoal(id, { amount: 10000 });
    loadGoals();
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-white tracking-tight">Financial Goals & Sufficiency</h1>
          <p className="text-xs text-slate-400 mt-1">Track wealth accumulation milestones with automated savings sufficiency forecasting.</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold flex items-center gap-2 transition"
        >
          <Plus className="w-4 h-4" /> New Financial Goal
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {goals.map(g => (
          <div key={g.id} className="glass-panel rounded-3xl p-6 border border-slate-800 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="font-bold text-sm text-white">{g.name}</h3>
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${g.sufficiency_status === 'ahead' || g.sufficiency_status === 'on_track' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'}`}>
                {g.sufficiency_status.replace('_', ' ')}
              </span>
            </div>

            <div>
              <div className="flex justify-between text-xs font-semibold text-slate-300 mb-1.5">
                <span>Progress: {g.percentage_completed}%</span>
                <span className="mono">₹{g.current_amount.toLocaleString('en-IN')} / ₹{g.target_amount.toLocaleString('en-IN')}</span>
              </div>
              <div className="w-full h-2.5 bg-slate-800 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-indigo-500 to-emerald-400 rounded-full transition-all duration-500"
                  style={{ width: `${g.percentage_completed}%` }}
                />
              </div>
            </div>

            <div className="text-xs text-slate-400 space-y-1">
              <p>Monthly Savings: <span className="font-bold text-white mono">₹{g.monthly_contribution.toLocaleString('en-IN')}/mo</span></p>
              <p>Target Date: <span className="mono text-slate-300">{g.target_date}</span></p>
            </div>

            <button
              onClick={() => handleContribute(g.id)}
              className="w-full py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold transition"
            >
              + Quick Deposit (₹10,000)
            </button>
          </div>
        ))}
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="glass-panel rounded-3xl p-6 border border-slate-800 w-full max-w-md space-y-4">
            <h3 className="font-extrabold text-base text-white">Create Goal</h3>
            <form onSubmit={handleCreate} className="space-y-3 text-xs">
              <div>
                <label className="block text-slate-300 font-bold mb-1">Goal Name</label>
                <input type="text" value={name} onChange={e => setName(e.target.value)} required className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white" placeholder="e.g. Europe Trip" />
              </div>
              <div>
                <label className="block text-slate-300 font-bold mb-1">Target Amount (₹)</label>
                <input type="number" value={targetAmt} onChange={e => setTargetAmt(Number(e.target.value))} required className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white" />
              </div>
              <div>
                <label className="block text-slate-300 font-bold mb-1">Initial Saved (₹)</label>
                <input type="number" value={currentAmt} onChange={e => setCurrentAmt(Number(e.target.value))} className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white" />
              </div>
              <div>
                <label className="block text-slate-300 font-bold mb-1">Monthly Contribution (₹)</label>
                <input type="number" value={monthlyContrib} onChange={e => setMonthlyContrib(Number(e.target.value))} className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white" />
              </div>
              <div className="flex justify-end gap-2 pt-2">
                <button type="button" onClick={() => setShowModal(false)} className="px-4 py-2 rounded-xl bg-slate-800 text-slate-300">Cancel</button>
                <button type="submit" className="px-5 py-2 rounded-xl bg-indigo-600 text-white font-bold">Save Goal</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
""")

    # 5. Data Import Page
    write_file("frontend/src/pages/imports/DataImportPage.tsx", """
import React, { useState, useEffect } from 'react';
import { api } from '../../services/api';
import { FileSpreadsheet, Upload, CheckCircle2, AlertTriangle, ArrowRight } from 'lucide-react';
import { FinancialAccount } from '../../types';

export const DataImportPage: React.FC = () => {
  const [accounts, setAccounts] = useState<FinancialAccount[]>([]);
  const [selectedAcc, setSelectedAcc] = useState<number>(0);
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  useEffect(() => {
    api.getAccounts().then(a => {
      setAccounts(a);
      if (a.length > 0) setSelectedAcc(a[0].id);
    });
  }, []);

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file || !selectedAcc) return;

    setLoading(true);
    const fd = new FormData();
    fd.append('account_id', String(selectedAcc));
    fd.append('file', file);

    try {
      const res = await fetch('/api/v1/imports/upload', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('finsight_token')}`
        },
        body: fd
      });
      const data = await res.json();
      setResult(data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-black text-white tracking-tight">Data Import & Statement Ingestion</h1>
        <p className="text-xs text-slate-400 mt-1">Upload CSV, Excel, or JSON bank statements for automated parsing, deduplication, and AI categorization.</p>
      </div>

      <div className="glass-panel rounded-3xl p-8 border border-slate-800 space-y-6">
        <form onSubmit={handleUpload} className="space-y-4 text-xs">
          <div>
            <label className="block text-slate-300 font-bold mb-1">Target Financial Account</label>
            <select
              value={selectedAcc}
              onChange={e => setSelectedAcc(Number(e.target.value))}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white"
            >
              {accounts.map(a => <option key={a.id} value={a.id}>{a.name} ({a.institution_name})</option>)}
            </select>
          </div>

          <div className="border-2 border-dashed border-slate-800 hover:border-indigo-500 rounded-2xl p-8 text-center bg-slate-950/40 cursor-pointer transition">
            <Upload className="w-8 h-8 text-indigo-400 mx-auto mb-2" />
            <p className="font-bold text-slate-200">Select Bank Statement File</p>
            <p className="text-[11px] text-slate-500 mt-1">Supports .csv, .xlsx, .xls</p>
            <input
              type="file"
              accept=".csv,.xlsx,.xls"
              onChange={e => e.target.files && setFile(e.target.files[0])}
              className="mt-3 block mx-auto text-xs text-slate-400"
            />
          </div>

          <button
            type="submit"
            disabled={loading || !file}
            className="w-full py-3 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 text-white font-extrabold hover:from-indigo-500 hover:to-violet-500 shadow-lg shadow-indigo-600/30 transition disabled:opacity-50"
          >
            {loading ? 'Processing & Categorizing Records...' : 'Execute Import Pipeline'}
          </button>
        </form>

        {result && (
          <div className="p-4 rounded-2xl bg-slate-900 border border-slate-800 space-y-3 animate-in fade-in">
            <div className="flex items-center justify-between">
              <span className="font-bold text-xs text-emerald-400 flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4" /> Import Completed Successfully
              </span>
              <span className="mono text-xs text-slate-400">{result.imported_records} / {result.total_records} records</span>
            </div>
            <div className="space-y-1.5 pt-2 border-t border-slate-800 text-xs">
              {result.preview?.map((p: any, i: number) => (
                <div key={i} className="flex justify-between py-1 border-b border-slate-800/40 text-slate-300">
                  <span>{p.description}</span>
                  <span className="mono font-bold text-indigo-400">{p.suggested_category}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
""")

    # 6. Admin & Model Monitoring Page (Module 18)
    write_file("frontend/src/pages/admin/AdminPage.tsx", """
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
""")

    # Update App.tsx to link all real pages
    write_file("frontend/src/App.tsx", """
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { AppLayout } from './components/layout/AppLayout';
import { LoginPage } from './pages/auth/LoginPage';
import { DashboardPage } from './pages/dashboard/DashboardPage';
import { ScenarioSimulatorPage } from './pages/scenarios/ScenarioSimulatorPage';
import { AssistantPage } from './pages/assistant/AssistantPage';
import { AccountsPage } from './pages/accounts/AccountsPage';
import { TransactionsPage } from './pages/transactions/TransactionsPage';
import { BudgetsPage } from './pages/budgets/BudgetsPage';
import { GoalsPage } from './pages/goals/GoalsPage';
import { DataImportPage } from './pages/imports/DataImportPage';
import { AdminPage } from './pages/admin/AdminPage';

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user } = useAuth();
  if (!user && !localStorage.getItem('finsight_token')) {
    return <Navigate to="/login" replace />;
  }
  return <>{children}</>;
};

export const App: React.FC = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/" element={<ProtectedRoute><AppLayout /></ProtectedRoute>}>
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard" element={<DashboardPage />} />
            <Route path="health" element={<DashboardPage />} />
            <Route path="cashflow" element={<DashboardPage />} />
            <Route path="scenarios" element={<ScenarioSimulatorPage />} />
            <Route path="assistant" element={<AssistantPage />} />
            <Route path="accounts" element={<AccountsPage />} />
            <Route path="transactions" element={<TransactionsPage />} />
            <Route path="budgets" element={<BudgetsPage />} />
            <Route path="goals" element={<GoalsPage />} />
            <Route path="recurring" element={<DashboardPage />} />
            <Route path="forecasts" element={<DashboardPage />} />
            <Route path="analytics" element={<DashboardPage />} />
            <Route path="anomalies" element={<DashboardPage />} />
            <Route path="imports" element={<DataImportPage />} />
            <Route path="reports" element={<DashboardPage />} />
            <Route path="admin" element={<AdminPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};
""")

    print("Phase 7 all frontend pages built successfully!")

if __name__ == "__main__":
    build_remaining_pages()
