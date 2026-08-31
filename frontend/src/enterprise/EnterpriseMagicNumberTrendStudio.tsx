import React, { useState } from "react";
import { TrendingUp, DollarSign, Target, Award } from "lucide-react";

export const EnterpriseMagicNumberTrendStudio: React.FC = () => {
  const quarters = [
    { quarter: "Q1 2026", arr: "$850,000", spend: "$620,000", magic: "1.37x", rating: "World Class" },
    { quarter: "Q2 2026", arr: "$1,120,000", spend: "$780,000", magic: "1.43x", rating: "World Class" },
    { quarter: "Q3 2026 (Est.)", arr: "$1,450,000", spend: "$950,000", magic: "1.52x", rating: "World Class" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-emerald-400" />
            SaaS Magic Number & Go-To-Market Efficiency
          </h3>
          <p className="text-xs text-slate-400">Quarterly net new ARR added per dollar of sales & marketing expenditure</p>
        </div>
      </div>

      <div className="space-y-3">
        {quarters.map((q, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{q.quarter}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Net New ARR: {q.arr} • S&M Spend: {q.spend}</div>
            </div>
            <div className="text-right">
              <span className="text-sm font-bold text-emerald-400">{q.magic}</span>
              <span className="text-[10px] text-slate-500 block">{q.rating}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
