import React, { useEffect, useState } from "react";
import { CheckCircle2 } from "lucide-react";
import { api } from "../../services/api";
import { Lead } from "../../types";

export const LeadsPage: React.FC = () => {
  const [leads, setLeads] = useState<Lead[]>([]);

  useEffect(() => { loadLeads(); }, []);
  const loadLeads = () => { api.getLeads().then(res => setLeads(res.data)).catch(console.error); };

  const handleConvert = async (leadId: string) => {
    await api.convertLead(leadId, { create_deal: true });
    loadLeads();
  };

  const handleQualify = async (leadId: string) => {
    await api.qualifyLead(leadId);
    loadLeads();
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-900">Leads & Scoring</h1>
        <p className="text-xs text-slate-500">Configurable multi-criteria lead qualification and 1-click deal conversion</p>
      </div>

      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-2xs">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200 text-slate-600 font-semibold">
              <th className="p-3.5">Lead Name</th>
              <th className="p-3.5">Company</th>
              <th className="p-3.5">Score & Grade</th>
              <th className="p-3.5">Status</th>
              <th className="p-3.5 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-slate-700">
            {leads.map(l => (
              <tr key={l.id} className="hover:bg-slate-50">
                <td className="p-3.5">
                  <div className="font-semibold text-slate-900">{l.first_name} {l.last_name}</div>
                  <div className="text-slate-400 text-[11px]">{l.email}</div>
                </td>
                <td className="p-3.5 font-medium text-slate-800">{l.company_name || "Independent"}</td>
                <td className="p-3.5">
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800">
                    Grade {l.qualification_grade} ({l.score}/100)
                  </span>
                </td>
                <td className="p-3.5">
                  <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-100 text-slate-700 uppercase">
                    {l.status}
                  </span>
                </td>
                <td className="p-3.5 text-right space-x-2">
                  {l.status !== "converted" ? (
                    <>
                      <button onClick={() => handleQualify(l.id)} className="px-2.5 py-1 bg-slate-100 text-slate-700 rounded text-xs font-semibold">Recalculate</button>
                      <button onClick={() => handleConvert(l.id)} className="px-2.5 py-1 bg-emerald-600 text-white rounded text-xs font-semibold">1-Click Convert ➔</button>
                    </>
                  ) : (
                    <span className="text-emerald-600 font-semibold text-xs inline-flex items-center gap-1">
                      <CheckCircle2 className="w-4 h-4" /> Converted
                    </span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
