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
