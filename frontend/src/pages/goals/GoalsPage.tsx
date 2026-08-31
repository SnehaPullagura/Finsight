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
