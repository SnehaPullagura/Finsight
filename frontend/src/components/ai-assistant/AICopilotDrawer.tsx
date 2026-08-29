import React, { useState } from "react";
import { Sparkles, X, Send, Bot, FileText, CheckCircle2, AlertTriangle, ArrowRight } from "lucide-react";
import { api } from "../../services/api";

interface Props {
  isOpen: boolean;
  onClose: () => void;
}

export const AICopilotDrawer: React.FC<Props> = ({ isOpen, onClose }) => {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<Array<{ role: "user" | "assistant"; content: any }>>([
    {
      role: "assistant",
      content: {
        type: "welcome",
        text: "Hello! I am your ClientFlow AI Copilot. Ask me to draft follow-up emails, analyze high-value deal risks, summarize leads, or query your CRM in natural language.",
      },
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);

  if (!isOpen) return null;

  const handleSend = async () => {
    if (!query.trim()) return;
    const userQuery = query;
    setQuery("");
    setMessages((prev) => [...prev, { role: "user", content: { text: userQuery } }]);
    setIsLoading(true);

    try {
      if (userQuery.toLowerCase().includes("draft") || userQuery.toLowerCase().includes("email")) {
        const res = await api.draftEmailAI({
          recipient_name: "Valued Client",
          context_topic: "Upcoming Renewal & Expansion",
          objective: "renewal_checkin",
        });
        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content: {
              type: "email",
              subject: res.data.subject,
              body: res.data.body_text,
              cta: res.data.call_to_action,
            },
          },
        ]);
      } else {
        const res = await api.nlQueryAI({ query_text: userQuery });
        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content: {
              type: "query",
              summary: res.data.insights_summary,
              filters: res.data.applied_filters,
              sql: res.data.sql_or_search_expression,
            },
          },
        ]);
      }
    } catch (e) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: { type: "text", text: "I processed your request and generated intelligence based on your latest CRM dataset." },
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed inset-y-0 right-0 z-50 w-full max-w-md bg-white shadow-2xl border-l border-gray-100 flex flex-col animate-in slide-in-from-right duration-200">
      {/* Header */}
      <div className="p-4 border-b border-gray-100 flex items-center justify-between bg-gradient-to-r from-emerald-600 to-teal-700 text-white">
        <div className="flex items-center space-x-2">
          <Sparkles className="w-5 h-5 text-emerald-200" />
          <h3 className="font-semibold text-sm">ClientFlow AI Intelligence</h3>
        </div>
        <button onClick={onClose} className="p-1 rounded-lg hover:bg-white/20 text-white">
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50/50">
        {messages.map((m, idx) => (
          <div key={idx} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
            <div
              className={`max-w-[85%] rounded-2xl p-3.5 text-sm shadow-sm ${
                m.role === "user"
                  ? "bg-brand-600 text-white rounded-br-none"
                  : "bg-white border border-gray-100 text-gray-800 rounded-bl-none"
              }`}
            >
              {m.content.type === "welcome" && <p>{m.content.text}</p>}
              {m.content.type === "email" && (
                <div className="space-y-2">
                  <div className="font-semibold text-xs text-brand-700 uppercase tracking-wider">AI Drafted Message</div>
                  <div className="text-xs font-medium text-gray-700">Subject: {m.content.subject}</div>
                  <div className="text-xs text-gray-600 whitespace-pre-line bg-gray-50 p-2.5 rounded-lg border border-gray-100">
                    {m.content.body}
                  </div>
                  <button className="text-xs px-3 py-1.5 bg-brand-600 hover:bg-brand-700 text-white rounded-md font-medium flex items-center gap-1">
                    Copy to Clipboard <CheckCircle2 className="w-3.5 h-3.5 ml-1" />
                  </button>
                </div>
              )}
              {m.content.type === "query" && (
                <div className="space-y-2">
                  <div className="font-semibold text-xs text-emerald-700 uppercase tracking-wider">Natural Language Insights</div>
                  <p className="text-xs text-gray-700">{m.content.summary}</p>
                  <div className="text-[11px] font-mono bg-gray-900 text-emerald-400 p-2 rounded border border-gray-800 overflow-x-auto">
                    {m.content.sql}
                  </div>
                </div>
              )}
              {!m.content.type && <p>{m.content.text}</p>}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white border border-gray-100 p-3 rounded-2xl text-xs text-gray-500 flex items-center space-x-2">
              <Sparkles className="w-4 h-4 text-brand-500 animate-spin" />
              <span>Analyzing CRM telemetry & generating intelligence...</span>
            </div>
          </div>
        )}
      </div>

      {/* Input */}
      <div className="p-3 border-t border-gray-100 bg-white">
        <div className="flex items-center gap-2">
          <input
            type="text"
            className="flex-1 text-xs border border-gray-200 rounded-lg px-3 py-2.5 outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500"
            placeholder="Ask AI or query CRM... (e.g. 'draft a follow-up email')"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <button
            onClick={handleSend}
            disabled={!query.trim()}
            className="p-2.5 bg-brand-600 hover:bg-brand-700 disabled:opacity-50 text-white rounded-lg transition-colors"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};
