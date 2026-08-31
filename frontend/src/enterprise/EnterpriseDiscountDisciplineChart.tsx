import React, { useState } from "react";
import { Percent, Award, ShieldAlert, CheckCircle2 } from "lucide-react";

export const EnterpriseDiscountDisciplineChart: React.FC = () => {
  const reps = [
    { name: "Alex Vance", deals: 14, avgDiscount: "6.2%", discipline: "High Discipline" },
    { name: "Sarah Connor", deals: 18, avgDiscount: "9.5%", discipline: "Disciplined" },
    { name: "John Wick", deals: 8, avgDiscount: "19.8%", discipline: "Manager Review" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Percent className="w-5 h-5 text-emerald-400" />
            Sales Rep Pricing & Discount Discipline
          </h3>
          <p className="text-xs text-slate-400">Average contract concessions and price preservation discipline by sales rep</p>
        </div>
      </div>

      <div className="space-y-3">
        {reps.map((r, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{r.name}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">{r.deals} deals closed • Avg Concession: {r.avgDiscount}</div>
            </div>
            <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${
              r.discipline === "High Discipline" ? "bg-emerald-950 text-emerald-400 border border-emerald-800" :
              r.discipline === "Disciplined" ? "bg-blue-950 text-blue-400 border border-blue-800" : "bg-amber-950 text-amber-400 border border-amber-800"
            }`}>
              {r.discipline}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
