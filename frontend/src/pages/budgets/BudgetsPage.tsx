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
