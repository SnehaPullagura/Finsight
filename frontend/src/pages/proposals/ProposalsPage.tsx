import React, { useEffect, useState } from "react";
import { FileCheck, CheckCircle2 } from "lucide-react";
import { api } from "../../services/api";
import { Proposal } from "../../types";

export const ProposalsPage: React.FC = () => {
  const [proposals, setProposals] = useState<Proposal[]>([]);

  useEffect(() => {
    api.getProposals().then(res => setProposals(res.data)).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-900">Proposals & SOWs</h1>
        <p className="text-xs text-slate-500">Interactive proposals, line items, and customer acceptance</p>
      </div>

      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-2xs">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-50 text-slate-600 font-semibold border-b">
            <tr>
              <th className="p-3.5">Proposal #</th>
              <th className="p-3.5">Title</th>
              <th className="p-3.5">Total Value</th>
              <th className="p-3.5">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-slate-700">
            {proposals.map(p => (
              <tr key={p.id} className="hover:bg-slate-50">
                <td className="p-3.5 font-semibold text-slate-900">{p.proposal_number}</td>
                <td className="p-3.5">{p.title}</td>
                <td className="p-3.5 font-bold text-emerald-600">${Number(p.total_amount).toLocaleString()}</td>
                <td className="p-3.5">
                  <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-100 text-emerald-800 uppercase">{p.status}</span>
                </td>
              </tr>
            ))}
            {proposals.length === 0 && <tr><td colSpan={4} className="p-8 text-center text-slate-400">No proposals generated yet.</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  );
};
