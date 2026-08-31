import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. frontend/src/components/enterprise/InteractiveKanbanBoard.tsx
    write_file("frontend/src/components/enterprise/InteractiveKanbanBoard.tsx", """import React, { useState } from "react";
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
""")

    # 2. frontend/src/components/enterprise/ReportDesigner.tsx
    write_file("frontend/src/components/enterprise/ReportDesigner.tsx", """import React, { useState } from "react";
import { BarChart3, PieChart, LineChart, Table, Download, RefreshCw } from "lucide-react";
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

const SAMPLE_CHART_DATA = [
  { month: "Jan", revenue: 145000, deals: 12 },
  { month: "Feb", revenue: 198000, deals: 16 },
  { month: "Mar", revenue: 240000, deals: 21 },
  { month: "Apr", revenue: 215000, deals: 18 },
  { month: "May", revenue: 280000, deals: 24 },
  { month: "Jun", revenue: 350000, deals: 29 }
];

export const ReportDesigner: React.FC = () => {
  const [metric, setMetric] = useState<"revenue" | "deals">("revenue");
  const [chartType, setChartType] = useState<"bar" | "line">("bar");

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-emerald-400" />
            Executive Report & Visual Analytics Studio
          </h3>
          <p className="text-xs text-slate-400">Configure customized cross-sectional telemetry and pipeline conversions</p>
        </div>
        <div className="flex items-center gap-3">
          <select
            value={metric}
            onChange={e => setMetric(e.target.value as any)}
            className="bg-slate-800 border border-slate-700 text-xs text-white rounded-lg px-3 py-1.5 focus:outline-none"
          >
            <option value="revenue">Closed Revenue ($)</option>
            <option value="deals">Deals Won (Count)</option>
          </select>
        </div>
      </div>

      <div className="h-64 bg-slate-950 p-4 rounded-xl border border-slate-800">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={SAMPLE_CHART_DATA}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis dataKey="month" stroke="#64748b" fontSize={11} />
            <YAxis stroke="#64748b" fontSize={11} tickFormatter={val => metric === "revenue" ? `$${val/1000}k` : val} />
            <Tooltip
              contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", borderRadius: "8px", fontSize: "11px" }}
              itemStyle={{ color: "#10b981" }}
            />
            <Bar dataKey={metric} fill="#10b981" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
""")

    print("Created InteractiveKanbanBoard and ReportDesigner.")

if __name__ == '__main__':
    run()
