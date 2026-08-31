import React, { useState } from "react";
import { ShieldAlert, BookOpen, CheckCircle2, FileText, ChevronRight } from "lucide-react";

export const EnterpriseObjectionBattlecards: React.FC = () => {
  const cards = [
    {
      title: "Price Objection / Budget Tightness",
      category: "Pricing",
      talkingPoints: [
        "Present 3-year Total Cost of Ownership (TCO) advantage vs Salesforce / HubSpot",
        "Demonstrate 4.5 hours saved per sales rep per week via automated workflows",
        "Offer flexible quarterly ramp billing structure"
      ]
    },
    {
      title: "Competitor Comparison: Salesforce Enterprise",
      category: "Competitor Displacement",
      talkingPoints: [
        "100% native multi-tenant data isolation with zero shared-tenant leakage",
        "Includes full CPQ, AI Copilot, and DAG Workflows without expensive tier add-ons",
        "2-week rapid deployment vs 6-9 months typical implementation timeline"
      ]
    }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-emerald-400" />
            Sales Objection & Competitor Battlecards
          </h3>
          <p className="text-xs text-slate-400">Battle-tested responses, objection handling frameworks, and architectural differentiators</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {cards.map((card, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-5 rounded-xl space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-white">{card.title}</span>
              <span className="text-[10px] bg-slate-800 text-purple-400 px-2 py-0.5 rounded uppercase font-semibold">{card.category}</span>
            </div>
            <ul className="space-y-2 text-xs text-slate-300">
              {card.talkingPoints.map((tp, i) => (
                <li key={i} className="flex items-start gap-2">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 shrink-0 mt-0.5" />
                  <span>{tp}</span>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
};
