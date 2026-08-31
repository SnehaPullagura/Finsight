import React, { useState } from "react";
import { DollarSign, User, Building, Calendar, CheckCircle2, Clock, MoreVertical, Plus } from "lucide-react";

interface DealCard {
  id: string;
  name: string;
  company: string;
  amount: number;
  probability: number;
  stage: string;
  owner: string;
  slaDays: number;
}

const INITIAL_DEALS: DealCard[] = [
  { id: "d-101", name: "Global Enterprise License", company: "Wayne Enterprises", amount: 250000, probability: 80, stage: "negotiation", owner: "Sarah Connor", slaDays: 3 },
  { id: "d-102", name: "Cloud Infrastructure Integration", company: "Stark Industries", amount: 180000, probability: 60, stage: "proposal", owner: "Alex Vance", slaDays: 6 },
  { id: "d-103", name: "Cybersecurity Suite Rollout", company: "Cyberdyne Systems", amount: 95000, probability: 40, stage: "scoping", owner: "John Wick", slaDays: 2 },
  { id: "d-104", name: "Custom Workflow Automation", company: "Oscorp Global", amount: 120000, probability: 90, stage: "contract", owner: "Sarah Connor", slaDays: 1 }
];

export const EnterprisePipelineKanban: React.FC = () => {
  const [deals, setDeals] = useState<DealCard[]>(INITIAL_DEALS);

  const columns = [
    { id: "scoping", label: "Scoping & Discovery", color: "border-blue-500/50" },
    { id: "proposal", label: "Proposal & Pricing", color: "border-amber-500/50" },
    { id: "negotiation", label: "Executive Negotiation", color: "border-purple-500/50" },
    { id: "contract", label: "Legal & Contract", color: "border-emerald-500/50" }
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white">Enterprise Pipeline Kanban</h2>
          <p className="text-xs text-slate-400">Interactive stage management with SLA indicators and probability weighting</p>
        </div>
        <button className="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-500 text-white px-3 py-1.5 rounded-lg text-xs font-semibold shadow-lg transition-colors">
          <Plus className="w-4 h-4" />
          Create Deal
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {columns.map(col => {
          const colDeals = deals.filter(d => d.stage === col.id);
          const colTotal = colDeals.reduce((sum, d) => sum + d.amount, 0);

          return (
            <div key={col.id} className={`bg-slate-900 border ${col.color} rounded-xl p-4 flex flex-col min-h-[500px]`}>
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <span className="text-xs font-bold text-white uppercase tracking-wider">{col.label}</span>
                <span className="text-xs bg-slate-800 text-slate-300 px-2 py-0.5 rounded-full">{colDeals.length}</span>
              </div>
              <div className="text-xs text-emerald-400 font-semibold my-2">
                ${colTotal.toLocaleString()} pipeline
              </div>

              <div className="space-y-3 mt-2 flex-1">
                {colDeals.map(deal => (
                  <div key={deal.id} className="bg-slate-950 border border-slate-800 hover:border-slate-700 p-3 rounded-lg shadow space-y-2 cursor-pointer transition-all">
                    <div className="text-xs font-bold text-white line-clamp-1">{deal.name}</div>
                    <div className="text-[11px] text-slate-400 flex items-center gap-1">
                      <Building className="w-3 h-3 text-slate-500" />
                      {deal.company}
                    </div>
                    <div className="flex items-center justify-between pt-2 border-t border-slate-800/60 text-[11px]">
                      <span className="font-bold text-emerald-400">${deal.amount.toLocaleString()}</span>
                      <span className="text-slate-400 flex items-center gap-1">
                        <Clock className="w-3 h-3 text-amber-400" />
                        {deal.slaDays}d in stage
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
