import React, { useState } from "react";
import { CheckSquare, ShieldCheck, AlertCircle, Award, CheckCircle2 } from "lucide-react";

export const EnterpriseMEDDICScorecard: React.FC = () => {
  const [criteria, setCriteria] = useState([
    { key: "metrics", label: "Metrics (Quantified Economic Impact)", weight: 15, checked: true },
    { key: "economic_buyer", label: "Economic Buyer (Access to Decision Maker)", weight: 20, checked: true },
    { key: "decision_criteria", label: "Decision Criteria (Technical & Business)", weight: 10, checked: true },
    { key: "decision_process", label: "Decision Process (Step-by-Step Approval)", weight: 10, checked: true },
    { key: "paper_process", label: "Paper Process (Legal & Procurement)", weight: 15, checked: false },
    { key: "identify_pain", label: "Identify Pain (Compelling Event & Cost of Inaction)", weight: 10, checked: true },
    { key: "champion", label: "Champion (Internal Advocate with Clout)", weight: 15, checked: true },
    { key: "competition", label: "Competition (Identified & Differentiated)", weight: 5, checked: true }
  ]);

  const totalScore = criteria.filter(c => c.checked).reduce((sum, c) => sum + c.weight, 0);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            MEDDPICC Deal Qualification Scorecard
          </h3>
          <p className="text-xs text-slate-400">Enterprise sales qualification framework to assess deal closing probability and risk</p>
        </div>
        <div className="text-right">
          <span className="text-[11px] text-slate-400 font-medium">Qualification Score</span>
          <div className="text-2xl font-bold text-emerald-400">{totalScore} / 100</div>
        </div>
      </div>

      <div className="space-y-2.5">
        {criteria.map(c => (
          <div key={c.key} className={`p-3 rounded-lg border flex items-center justify-between transition-colors ${
            c.checked ? "bg-slate-950 border-emerald-900/50" : "bg-slate-950/60 border-slate-800"
          }`}>
            <div className="flex items-center gap-3">
              <input
                type="checkbox"
                checked={c.checked}
                onChange={() => {
                  setCriteria(criteria.map(item => item.key === c.key ? { ...item, checked: !item.checked } : item));
                }}
                className="w-4 h-4 rounded text-emerald-600 focus:ring-emerald-500 bg-slate-900 border-slate-700"
              />
              <span className="text-xs font-medium text-white">{c.label}</span>
            </div>
            <span className="text-xs font-bold text-slate-400">{c.weight} pts</span>
          </div>
        ))}
      </div>
    </div>
  );
};
