import React, { useState } from 'react';
import { api } from '../../services/api';
import { Bot, Send, Sparkles, User, HelpCircle, CheckCircle2, ArrowRight } from 'lucide-react';

export const AssistantPage: React.FC = () => {
  const [messages, setMessages] = useState<Array<{ sender: 'user' | 'ai'; text: string; card?: any; facts?: string[] }>>([
    {
      sender: 'ai',
      text: 'Hello! I am your FinSight AI Financial Assistant. I am directly grounded in your real transaction data, accounts, and health metrics. What financial decision would you like to evaluate today?'
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async (queryText?: string) => {
    const q = queryText || input;
    if (!q.trim()) return;

    const newMsgs = [...messages, { sender: 'user' as const, text: q }];
    setMessages(newMsgs);
    if (!queryText) setInput('');
    setLoading(true);

    try {
      const res = await api.queryAssistant(q);
      setMessages([
        ...newMsgs,
        {
          sender: 'ai' as const,
          text: res.answer,
          card: res.data_card,
          facts: res.grounded_facts
        }
      ]);
    } catch (err: any) {
      setMessages([
        ...newMsgs,
        { sender: 'ai' as const, text: 'Apologies, I encountered an issue analyzing your data. Please try again.' }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const SUGGESTIONS = [
    "What is my Financial Health Score?",
    "Can I afford a ₹50,000 purchase this month?",
    "Why did my expenses increase recently?",
    "How much should I allocate to emergency fund?"
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-4">
      {/* Header */}
      <div className="flex items-center gap-3 pb-3 border-b border-slate-800">
        <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-indigo-600 to-violet-600 flex items-center justify-center text-white shadow-lg shadow-indigo-600/30">
          <Bot className="w-5 h-5" />
        </div>
        <div>
          <h1 className="text-xl font-extrabold text-white">Data-Grounded AI Financial Assistant</h1>
          <p className="text-xs text-slate-400">Contextual financial intelligence powered by your live data records.</p>
        </div>
      </div>

      {/* Chat Messages Container */}
      <div className="glass-panel rounded-3xl p-6 border border-slate-800 min-h-[500px] max-h-[600px] flex flex-col justify-between overflow-hidden">
        <div className="overflow-y-auto space-y-4 pr-2 flex-1">
          {messages.map((m, idx) => (
            <div key={idx} className={`flex gap-3 ${m.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
              {m.sender === 'ai' && (
                <div className="w-8 h-8 rounded-xl bg-indigo-600 flex items-center justify-center text-white shrink-0">
                  <Bot className="w-4 h-4" />
                </div>
              )}
              <div className={`max-w-xl rounded-2xl p-4 text-xs leading-relaxed ${m.sender === 'user' ? 'bg-indigo-600 text-white font-medium' : 'bg-slate-900/80 border border-slate-800 text-slate-200'}`}>
                <p className="whitespace-pre-wrap">{m.text}</p>

                {/* Grounded Facts Badge */}
                {m.facts && m.facts.length > 0 && (
                  <div className="mt-3 pt-2.5 border-t border-slate-800/80 flex flex-wrap gap-2 text-[10px] text-slate-400">
                    <span className="font-bold text-indigo-400">Grounded Facts:</span>
                    {m.facts.map((f, i) => (
                      <span key={i} className="px-2 py-0.5 rounded-md bg-slate-950 border border-slate-800">{f}</span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex gap-3 items-center text-xs text-slate-400">
              <div className="w-8 h-8 rounded-xl bg-indigo-600/50 flex items-center justify-center text-white animate-pulse">
                <Bot className="w-4 h-4" />
              </div>
              <span>Analyzing financial records & projections...</span>
            </div>
          )}
        </div>

        {/* Suggested Prompts */}
        <div className="pt-4 border-t border-slate-800/80 mt-4 space-y-3">
          <div className="flex flex-wrap gap-2">
            {SUGGESTIONS.map((s, i) => (
              <button
                key={i}
                onClick={() => handleSend(s)}
                className="px-3 py-1.5 rounded-full bg-slate-900 hover:bg-slate-800 border border-slate-800 text-[11px] text-slate-300 transition"
              >
                {s}
              </button>
            ))}
          </div>

          {/* Input Box */}
          <form
            onSubmit={e => { e.preventDefault(); handleSend(); }}
            className="flex items-center gap-2 bg-slate-950 border border-slate-800 rounded-2xl p-2 focus-within:border-indigo-500 transition"
          >
            <input
              type="text"
              value={input}
              onChange={e => setInput(e.target.value)}
              placeholder="Ask a question about your spending, affordability, or forecasts..."
              className="flex-1 bg-transparent px-3 py-1.5 text-xs text-white placeholder-slate-500 focus:outline-none"
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="p-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white transition"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};
