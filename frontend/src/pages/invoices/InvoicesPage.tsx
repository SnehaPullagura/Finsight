import React, { useEffect, useState } from "react";
import { Receipt } from "lucide-react";
import { api } from "../../services/api";
import { Invoice } from "../../types";

export const InvoicesPage: React.FC = () => {
  const [invoices, setInvoices] = useState<Invoice[]>([]);

  useEffect(() => {
    api.getInvoices().then(res => setInvoices(res.data)).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-900">Invoices & Billing</h1>
        <p className="text-xs text-slate-500">Payment statuses, due dates, and accounting records</p>
      </div>

      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-2xs">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-50 text-slate-600 font-semibold border-b">
            <tr>
              <th className="p-3.5">Invoice #</th>
              <th className="p-3.5">Due Date</th>
              <th className="p-3.5">Total Amount</th>
              <th className="p-3.5">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-slate-700">
            {invoices.map(i => (
              <tr key={i.id} className="hover:bg-slate-50">
                <td className="p-3.5 font-semibold text-slate-900">{i.invoice_number}</td>
                <td className="p-3.5 text-slate-500">{i.due_date}</td>
                <td className="p-3.5 font-bold text-slate-900">${Number(i.total_amount).toLocaleString()}</td>
                <td className="p-3.5">
                  <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-100 text-emerald-800 uppercase">{i.payment_status}</span>
                </td>
              </tr>
            ))}
            {invoices.length === 0 && <tr><td colSpan={4} className="p-8 text-center text-slate-400">No invoices generated yet.</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  );
};
