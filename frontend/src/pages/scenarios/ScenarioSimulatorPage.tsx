import React, { useState, useEffect } from 'react';
import { api } from '../../services/api';
import { SlidersHorizontal, Plus, ArrowRight, CheckCircle, AlertCircle, Sparkles } from 'lucide-react';
import { Scenario } from '../../types';

export const ScenarioSimulatorPage: React.FC = () => {
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [baseCase, setBaseCase] = useState<any>(null);
  const [verdict, setVerdict] = useState<string>('');
  
  // Interactive Simulation Form States
  const [name, setName] = useState('New Car Loan & Job Switch');
  const [incomeDelta, setIncomeDelta] = useState(25000);
  const [expenseDelta, setExpenseDelta] = useState(5000);
  const [lumpSum, setLumpSum] = useState(200000);
  const [loanAmount, setLoanAmount] = useState(800000);
  const [tenure, setTenure] = useState(48);
  const [rate, setRate] = useState(9.5);
  const [loading, setLoading] = useState(false);

  const loadData = () => {
    api.getScenariosCompare().then(res => {
      setBaseCase(res.base_case);
      setScenarios(res.scenarios);
      setVerdict(res.comparison_verdict);
    });
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleSimulate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.createScenario({
        name,
        monthly_income_delta: Number(incomeDelta),
        monthly_expense_delta: Number(expenseDelta),
        one_time_lump_sum: Number(lumpSum),
        loan_amount: Number(loanAmount),
        loan_tenure_months: Number(tenure),
        loan_interest_rate: Number(rate)
      });
      loadData();
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 text-indigo-400 text-xs font-bold border border-indigo-500/20 mb-2">
            <Sparkles className="w-3.5 h-3.5" /> Key FinSight Differentiator
          </div>
          <h1 className="text-2xl font-black text-white tracking-tight">What-If Financial Scenario Simulator</h1>
          <p className="text-xs text-slate-400 mt-1">
            Modify variables (income raises, rent increases, loans, down payments) and recalculate cash flows, 12-month balances, and health score deltas.
          </p>
        </div>
      </div>

      {/* Simulator Workspace Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Interactive Controls Form */}
        <div className="glass-panel rounded-3xl p-6 border border-slate-800 space-y-5">
          <div className="flex items-center gap-2 pb-3 border-b border-slate-800">
            <SlidersHorizontal className="w-4 h-4 text-indigo-400" />
            <h3 className="font-extrabold text-sm text-slate-200 uppercase tracking-wider">Configure Variables</h3>
          </div>

          <form onSubmit={handleSimulate} className="space-y-4 text-xs">
            <div>
              <label className="font-bold text-slate-300 block mb-1">Scenario Title</label>
              <input
                type="text"
                value={name}
                onChange={e => setName(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-slate-100 focus:outline-none focus:border-indigo-500"
                required
              />
            </div>

            <div>
              <div className="flex justify-between font-bold text-slate-300 mb-1">
                <span>Monthly Income Delta (+/-)</span>
                <span className="mono text-indigo-400">₹{incomeDelta.toLocaleString('en-IN')}</span>
              </div>
              <input
                type="range"
                min="-50000"
                max="100000"
                step="5000"
                value={incomeDelta}
                onChange={e => setIncomeDelta(Number(e.target.value))}
                className="w-full accent-indigo-500"
              />
            </div>

            <div>
              <div className="flex justify-between font-bold text-slate-300 mb-1">
                <span>Monthly Expense Delta (+/-)</span>
                <span className="mono text-rose-400">₹{expenseDelta.toLocaleString('en-IN')}</span>
              </div>
              <input
                type="range"
                min="-20000"
                max="50000"
                step="2000"
                value={expenseDelta}
                onChange={e => setExpenseDelta(Number(e.target.value))}
                className="w-full accent-rose-500"
              />
            </div>

            <div>
              <label className="font-bold text-slate-300 block mb-1">One-Time Lump Sum Outlay (₹)</label>
              <input
                type="number"
                value={lumpSum}
                onChange={e => setLumpSum(Number(e.target.value))}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-slate-100 focus:outline-none focus:border-indigo-500"
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="font-bold text-slate-300 block mb-1">Loan Principal (₹)</label>
                <input
                  type="number"
                  value={loanAmount}
                  onChange={e => setLoanAmount(Number(e.target.value))}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-slate-100"
                />
              </div>
              <div>
                <label className="font-bold text-slate-300 block mb-1">Tenure (Months)</label>
                <input
                  type="number"
                  value={tenure}
                  onChange={e => setTenure(Number(e.target.value))}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-slate-100"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 text-white font-extrabold hover:from-indigo-500 hover:to-violet-500 shadow-lg shadow-indigo-600/30 transition mt-2"
            >
              {loading ? 'Recalculating Projections...' : 'Simulate & Save Scenario'}
            </button>
          </form>
        </div>

        {/* Side-by-Side Comparison Matrix */}
        <div className="lg:col-span-2 glass-panel rounded-3xl p-6 border border-slate-800 space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800">
            <div>
              <h3 className="font-extrabold text-sm text-slate-200 uppercase tracking-wider">Side-by-Side Scenario Outcomes</h3>
              <p className="text-xs text-indigo-400 font-semibold mt-0.5">{verdict}</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Base Case Card */}
            <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-3">
              <div className="flex items-center justify-between">
                <span className="font-extrabold text-xs text-slate-400 uppercase tracking-wider">Baseline Status Quo</span>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-800 text-slate-300">Base</span>
              </div>
              <div className="space-y-1.5 text-xs">
                <div className="flex justify-between"><span className="text-slate-400">Current Balance:</span><span className="mono font-bold text-white">₹{baseCase?.current_balance?.toLocaleString('en-IN')}</span></div>
                <div className="flex justify-between"><span className="text-slate-400">6M Projected:</span><span className="mono font-bold text-white">₹{baseCase?.projected_6m_balance?.toLocaleString('en-IN')}</span></div>
                <div className="flex justify-between"><span className="text-slate-400">12M Projected:</span><span className="mono font-bold text-white">₹{baseCase?.projected_12m_balance?.toLocaleString('en-IN')}</span></div>
                <div className="flex justify-between"><span className="text-slate-400">Health Score:</span><span className="mono font-bold text-emerald-400">{baseCase?.baseline_health_score}/100</span></div>
              </div>
            </div>

            {/* Simulated Scenarios */}
            {scenarios.map(sc => (
              <div key={sc.id} className="p-4 rounded-2xl bg-indigo-950/30 border border-indigo-500/20 space-y-3 relative overflow-hidden">
                <div className="flex items-center justify-between">
                  <span className="font-extrabold text-xs text-white truncate pr-2">{sc.name}</span>
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${sc.is_feasible ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'}`}>
                    {sc.is_feasible ? 'Feasible' : 'High Risk'}
                  </span>
                </div>
                <div className="space-y-1.5 text-xs">
                  {sc.calculated_monthly_emi > 0 && (
                    <div className="flex justify-between"><span className="text-slate-400">Monthly EMI:</span><span className="mono font-bold text-rose-400">₹{sc.calculated_monthly_emi?.toLocaleString('en-IN')}</span></div>
                  )}
                  <div className="flex justify-between"><span className="text-slate-400">12M Projected:</span><span className="mono font-black text-white">₹{sc.projected_12m_balance?.toLocaleString('en-IN')}</span></div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Health Score Delta:</span>
                    <span className={`mono font-bold ${sc.health_score_delta >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                      {sc.health_score_delta >= 0 ? '+' : ''}{sc.health_score_delta} pts
                    </span>
                  </div>
                </div>
                <p className="text-[11px] text-slate-400 leading-snug pt-2 border-t border-slate-800/80">
                  {sc.feasibility_notes}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
