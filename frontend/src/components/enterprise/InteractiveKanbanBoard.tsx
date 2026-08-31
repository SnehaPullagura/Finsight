import React, { useState } from "react";
import { Plus, MoreVertical, DollarSign, User, Clock, ArrowRight, ShieldCheck, Tag } from "lucide-react";

interface KanbanCard {
  id: string;
  title: string;
  company: string;
  value: number;
  owner: string;
  stage_id: string;
  days_in_stage: number;
  priority: "low" | "medium" | "high";
}

interface KanbanStage {
  id: string;
  title: string;
  color: string;
  wip_limit: number;
}

const INITIAL_STAGES: KanbanStage[] = [
  { id: "stg-1", title: "Discovery & Qualification", color: "border-blue-500", wip_limit: 10 },
  { id: "stg-2", title: "Solution Proposal", color: "border-purple-500", wip_limit: 8 },
  { id: "stg-3", title: "Contract Negotiation", color: "border-amber-500", wip_limit: 5 },
  { id: "stg-4", title: "Closed Won", color: "border-emerald-500", wip_limit: 999 }
];

const INITIAL_CARDS: KanbanCard[] = [
  { id: "c-1", title: "Global Cloud Architecture", company: "Stark Industries", value: 250000, owner: "Alexander Vance", stage_id: "stg-3", days_in_stage: 4, priority: "high" },
  { id: "c-2", title: "AI Security Operations", company: "Wayne Enterprises", value: 450000, owner: "Alexander Vance", stage_id: "stg-2", days_in_stage: 12, priority: "medium" },
  { id: "c-3", title: "SAML Okta SSO Integration", company: "Cyberdyne Systems", value: 85000, owner: "Alexander Vance", stage_id: "stg-1", days_in_stage: 2, priority: "low" },
  { id: "c-4", title: "Omnichannel Contact Center", company: "Acme Corp", value: 160000, owner: "Alexander Vance", stage_id: "stg-4", days_in_stage: 1, priority: "high" }
];

export const InteractiveKanbanBoard: React.FC = () => {
  const [stages] = useState<KanbanStage[]>(INITIAL_STAGES);
  const [cards, setCards] = useState<KanbanCard[]>(INITIAL_CARDS);
  const [filterQuery, setFilterQuery] = useState("");

  const moveCard = (cardId: string, nextStageId: string) => {
    setCards(cards.map(c => c.id === cardId ? { ...c, stage_id: nextStageId, days_in_stage: 0 } : c));
  };

  const filteredCards = cards.filter(c => 
    c.title.toLowerCase().includes(filterQuery.toLowerCase()) ||
    c.company.toLowerCase().includes(filterQuery.toLowerCase())
  );

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <input
          type="text"
          placeholder="Filter deals by name or company..."
          value={filterQuery}
          onChange={e => setFilterQuery(e.target.value)}
          className="w-72 bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500"
        />
        <div className="text-xs text-slate-400">
          Total Pipeline: <strong className="text-white">${cards.reduce((sum, c) => sum + c.value, 0).toLocaleString()}</strong>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 overflow-x-auto pb-4">
        {stages.map(stg => {
          const stageCards = filteredCards.filter(c => c.stage_id === stg.id);
          const stageTotal = stageCards.reduce((sum, c) => sum + c.value, 0);

          return (
            <div key={stg.id} className={`bg-slate-900/90 border-t-4 ${stg.color} border-slate-800 rounded-xl p-3 space-y-3 min-w-[280px]`}>
              <div className="flex items-center justify-between pb-2 border-b border-slate-800 text-xs">
                <div className="font-bold text-white flex items-center gap-1.5">
                  <span>{stg.title}</span>
                  <span className="text-[10px] bg-slate-800 px-1.5 py-0.5 rounded text-slate-400">{stageCards.length}</span>
                </div>
                <div className="text-[11px] font-semibold text-emerald-400">${stageTotal.toLocaleString()}</div>
              </div>

              <div className="space-y-2.5 min-h-[300px]">
                {stageCards.map(card => (
                  <div key={card.id} className="bg-slate-950 p-3 rounded-lg border border-slate-800/80 shadow-md space-y-2 hover:border-slate-700 transition-all">
                    <div className="flex items-start justify-between">
                      <div className="font-bold text-xs text-white leading-tight">{card.title}</div>
                      <span className={`text-[9px] px-1.5 py-0.5 rounded font-semibold uppercase ${
                        card.priority === "high" ? "bg-rose-500/20 text-rose-400" :
                        card.priority === "medium" ? "bg-amber-500/20 text-amber-400" : "bg-blue-500/20 text-blue-400"
                      }`}>{card.priority}</span>
                    </div>

                    <div className="text-[11px] text-slate-400">{card.company}</div>

                    <div className="flex items-center justify-between pt-2 border-t border-slate-800/60 text-[11px]">
                      <div className="font-bold text-emerald-400">${card.value.toLocaleString()}</div>
                      <div className="text-slate-500 flex items-center gap-1">
                        <Clock className="w-3 h-3" /> {card.days_in_stage}d
                      </div>
                    </div>

                    {stg.id !== "stg-4" && (
                      <button
                        onClick={() => {
                          const currentIdx = stages.findIndex(s => s.id === stg.id);
                          if (currentIdx < stages.length - 1) {
                            moveCard(card.id, stages[currentIdx + 1].id);
                          }
                        }}
                        className="w-full py-1 mt-1 bg-slate-900 hover:bg-slate-800 text-[10px] text-slate-300 font-semibold rounded flex items-center justify-center gap-1 border border-slate-800"
                      >
                        <span>Advance Stage</span>
                        <ArrowRight className="w-3 h-3 text-emerald-400" />
                      </button>
                    )}
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
