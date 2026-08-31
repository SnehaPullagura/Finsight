import React, { useState } from "react";
import { Calendar, ShieldAlert, CheckCircle2, TrendingUp, AlertTriangle } from "lucide-react";

export const EnterprisePredictiveRenewalStudio: React.FC = () => {
  const renewals = [
    { name: "Acme Global Industries", arr: "$320,000", days: 45, prob: "94%", status: "Safe On-Track" },
    { name: "Stark Tech Enterprises", arr: "$250,000", days: 60, prob: "88%", status: "Safe On-Track" },
    { name: "Cyberdyne Systems", arr: "$140,000", days: 30, prob: "52%", status: "Moderate Risk" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Calendar className="w-5 h-5 text-emerald-400" />
            Predictive Contract Renewal & Retention Modeler
          </h3>
          <p className="text-xs text-slate-400">Algorithmic renewal probabilities based on product usage, NPS, and executive sponsor engagement</p>
        </div>
      </div>

      <div className="space-y-3">
        {renewals.map((r, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{r.name}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">
                ARR: {r.arr} • Renewing in {r.days} days • Probability: <span className="text-emerald-400 font-bold">{r.prob}</span>
              </div>
            </div>
            <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${
              r.status === "Safe On-Track" ? "bg-emerald-950 text-emerald-400 border border-emerald-800" : "bg-amber-950 text-amber-400 border border-amber-800"
            }`}>
              {r.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
