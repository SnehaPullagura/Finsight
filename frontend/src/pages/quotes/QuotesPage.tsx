import React, { useEffect, useState } from "react";
import { FileSpreadsheet } from "lucide-react";
import { api } from "../../services/api";
import { Quote } from "../../types";

export const QuotesPage: React.FC = () => {
  const [quotes, setQuotes] = useState<Quote[]>([]);

  useEffect(() => {
    api.getQuotes().then(res => setQuotes(res.data)).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-900">Quotes</h1>
        <p className="text-xs text-slate-500">Formal sales quotes and revision approvals</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {quotes.map(q => (
          <div key={q.id} className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs space-y-2">
            <h4 className="text-xs font-bold text-slate-900">{q.quote_number}</h4>
            <div className="text-xs font-bold text-emerald-600">${Number(q.total_amount).toLocaleString()}</div>
          </div>
        ))}
        {quotes.length === 0 && <div className="p-8 col-span-full text-center text-xs text-slate-400 bg-white rounded-xl border border-slate-200">No active quotes.</div>}
      </div>
    </div>
  );
};
