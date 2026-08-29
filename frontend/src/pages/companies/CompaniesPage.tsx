import React, { useEffect, useState } from "react";
import { Plus, Search, Building2 } from "lucide-react";
import { api } from "../../services/api";
import { Company } from "../../types";

export const CompaniesPage: React.FC = () => {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    api.getCompanies().then(res => setCompanies(res.data)).catch(console.error);
  }, []);

  const filtered = companies.filter(c => c.name.toLowerCase().includes(search.toLowerCase()));

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-900">Companies & Accounts</h1>
        <p className="text-xs text-slate-500">Corporate entities, parent-subsidiary hierarchies, and annual valuations</p>
      </div>

      <div className="flex items-center gap-3 bg-white p-3 rounded-xl border border-slate-200 shadow-2xs">
        <Search className="w-4 h-4 text-slate-400" />
        <input placeholder="Filter companies..." className="flex-1 text-xs outline-none" value={search} onChange={e => setSearch(e.target.value)} />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filtered.map(c => (
          <div key={c.id} className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs">
            <div className="flex items-center gap-3 mb-3">
              <div className="p-2 rounded-lg bg-purple-50 text-purple-600 border border-purple-100">
                <Building2 className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-sm font-bold text-slate-900">{c.name}</h3>
                <span className="text-[11px] text-slate-400">{c.domain || "no-domain.com"}</span>
              </div>
            </div>
            <div className="text-xs text-slate-600 space-y-1 pt-2 border-t border-slate-100">
              <div className="flex justify-between">
                <span className="text-slate-400">Industry:</span>
                <span className="font-semibold text-slate-700 capitalize">{c.industry || "General"}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Annual Revenue:</span>
                <span className="font-semibold text-emerald-600">${Number(c.annual_revenue || 0).toLocaleString()}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
