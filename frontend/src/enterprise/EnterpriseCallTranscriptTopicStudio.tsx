import React, { useState } from "react";
import { Mic, Sparkles, MessageSquare, CheckCircle2, TrendingUp } from "lucide-react";

export const EnterpriseCallTranscriptTopicStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Mic className="w-5 h-5 text-emerald-400" />
            AI Conversation Intelligence & Talk-to-Listen Cadence
          </h3>
          <p className="text-xs text-slate-400">NLP topic extraction and rep talk-time ratio analysis from recorded sales meetings</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Optimal 44% / 56%
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Rep Talk Ratio</span>
          <div className="text-2xl font-bold text-emerald-400">44.2%</div>
          <span className="text-[10px] text-slate-400">Target Benchmark: &lt; 48%</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Customer Talk Ratio</span>
          <div className="text-2xl font-bold text-white">55.8%</div>
          <span className="text-[10px] text-emerald-400">High Engagement Discovery</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Competitor Mentions</span>
          <div className="text-2xl font-bold text-amber-400">2 Mentions</div>
          <span className="text-[10px] text-slate-400">HubSpot & Salesforce CPQ</span>
        </div>
      </div>
    </div>
  );
};
