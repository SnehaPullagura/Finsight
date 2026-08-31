import React, { useState } from "react";
import { Sparkles, Bot, Send, MessageSquare, CheckCircle2, RefreshCw } from "lucide-react";

export const EnterpriseAICopilotStudio: React.FC = () => {
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Hello! I am ClientFlow AI Copilot. I can analyze your sales pipeline, predict quarterly finish, recommend pricing discounts, or draft contract renewal proposals. How can I assist you today?" }
  ]);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-emerald-400" />
            AI Copilot Studio & Natural Language Query Hub
          </h3>
          <p className="text-xs text-slate-400">Context-aware CRM generative assistant with multi-turn memory and action dispatch</p>
        </div>
      </div>

      <div className="bg-slate-950 border border-slate-800 rounded-xl p-4 min-h-[300px] flex flex-col justify-between space-y-4">
        <div className="space-y-3">
          {messages.map((m, idx) => (
            <div key={idx} className={`flex items-start gap-3 ${m.role === "assistant" ? "text-slate-300" : "text-white"}`}>
              <div className="w-7 h-7 rounded-lg bg-emerald-950 border border-emerald-800 flex items-center justify-center text-emerald-400 text-xs font-bold">
                AI
              </div>
              <div className="bg-slate-900 border border-slate-800 p-3 rounded-lg text-xs leading-relaxed max-w-lg">
                {m.content}
              </div>
            </div>
          ))}
        </div>

        <div className="flex items-center gap-2 pt-2 border-t border-slate-800">
          <input
            type="text"
            placeholder="Ask AI Copilot: 'What is our expected quarter finish based on Monte Carlo simulation?'"
            className="flex-1 bg-slate-900 border border-slate-800 text-white px-3 py-2 rounded-lg text-xs focus:outline-none focus:border-emerald-500"
          />
          <button className="bg-emerald-600 hover:bg-emerald-500 text-white p-2 rounded-lg text-xs font-semibold shadow transition-colors">
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};
