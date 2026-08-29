import React, { useEffect, useState } from "react";
import { LifeBuoy, AlertCircle, CheckCircle2 } from "lucide-react";
import { api } from "../../services/api";
import { Ticket } from "../../types";

export const SupportPage: React.FC = () => {
  const [tickets, setTickets] = useState<Ticket[]>([]);

  useEffect(() => {
    api.getTickets().then(res => setTickets(res.data)).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-900">Customer Support & SLA</h1>
        <p className="text-xs text-slate-500">Omnichannel tickets, SLA breach prevention, and resolution queues</p>
      </div>

      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-2xs">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-50 text-slate-600 font-semibold border-b">
            <tr>
              <th className="p-3.5">Ticket #</th>
              <th className="p-3.5">Subject</th>
              <th className="p-3.5">Priority</th>
              <th className="p-3.5">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-slate-700">
            {tickets.map(t => (
              <tr key={t.id} className="hover:bg-slate-50">
                <td className="p-3.5 font-semibold text-slate-900">{t.ticket_number}</td>
                <td className="p-3.5">{t.subject}</td>
                <td className="p-3.5">
                  <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${t.priority === 'urgent' ? 'bg-rose-100 text-rose-800' : 'bg-slate-100 text-slate-700'}`}>
                    {t.priority}
                  </span>
                </td>
                <td className="p-3.5">
                  <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-100 text-emerald-800 uppercase">{t.status}</span>
                </td>
              </tr>
            ))}
            {tickets.length === 0 && <tr><td colSpan={4} className="p-8 text-center text-slate-400">No support tickets in queue.</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  );
};
