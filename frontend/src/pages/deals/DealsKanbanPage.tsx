import React, { useEffect, useState } from "react";
import { ChevronRight } from "lucide-react";
import { api } from "../../services/api";
import { KanbanBoard } from "../../types";

export const DealsKanbanPage: React.FC = () => {
  const [board, setBoard] = useState<KanbanBoard | null>(null);

  useEffect(() => { loadBoard(); }, []);
  const loadBoard = () => { api.getKanbanBoard().then(res => setBoard(res.data)).catch(console.error); };

  const handleStageMove = async (dealId: string, targetStageId: string) => {
    await api.transitionDealStage(dealId, { stage_id: targetStageId });
    loadBoard();
  };

  if (!board) return <div className="p-8 text-center text-sm text-slate-500">Loading sales pipelines...</div>;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-900">{board.pipeline_name}</h1>
        <p className="text-xs text-slate-500">Advance deals across validated sales stages</p>
      </div>

      <div className="flex gap-4 overflow-x-auto pb-4">
        {board.columns.map((col, idx) => (
          <div key={col.stage_id} className="w-80 shrink-0 bg-slate-100/70 rounded-xl p-3 border border-slate-200/80 flex flex-col max-h-[75vh]">
            <div className="flex items-center justify-between mb-3 px-1">
              <div>
                <h4 className="text-xs font-bold text-slate-800">{col.stage_name}</h4>
                <div className="text-[10px] text-slate-400">{col.deal_count} deals • ${col.total_value.toLocaleString()}</div>
              </div>
              <span className="text-[10px] font-semibold px-2 py-0.5 rounded bg-white text-slate-600 border border-slate-200">
                {col.probability}%
              </span>
            </div>

            <div className="flex-1 overflow-y-auto space-y-2 pr-1">
              {col.deals.map(d => (
                <div key={d.id} className="bg-white p-3.5 rounded-lg border border-slate-200 shadow-2xs space-y-2">
                  <div className="flex justify-between items-start">
                    <h5 className="text-xs font-bold text-slate-900">{d.name}</h5>
                    <span className="text-xs font-bold text-emerald-600">${Number(d.value).toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between items-center text-[10px] text-slate-400 pt-2 border-t border-slate-100">
                    <span>{d.probability}% Prob.</span>
                    {idx < board.columns.length - 1 && (
                      <button
                        onClick={() => handleStageMove(d.id, board.columns[idx + 1].stage_id)}
                        className="px-2 py-0.5 bg-slate-50 hover:bg-emerald-50 text-slate-600 rounded border border-slate-200 text-[10px] font-medium flex items-center gap-0.5"
                      >
                        Advance <ChevronRight className="w-3 h-3" />
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
