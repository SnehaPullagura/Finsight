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
