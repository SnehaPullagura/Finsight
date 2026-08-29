import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. frontend/src/index.css
    write_file("frontend/src/index.css", """@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen", "Ubuntu", "Cantarell", "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f8fafc;
}

/* Custom modern scrollbars */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
""")

    # 2. frontend/src/components/common/GlobalSearchModal.tsx
    write_file("frontend/src/components/common/GlobalSearchModal.tsx", """import React, { useState, useEffect } from "react";
import { Search, X, User, Building2, Target, DollarSign, LifeBuoy, ArrowRight } from "lucide-react";
import { api } from "../../services/api";
import { useNavigate } from "react-router-dom";

interface Props {
  isOpen: boolean;
  onClose: () => void;
}

export const GlobalSearchModal: React.FC<Props> = ({ isOpen, onClose }) => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    if (!query.trim()) {
      setResults([]);
      return;
    }
    const timer = setTimeout(() => {
      setIsLoading(true);
      api.globalSearch(query)
        .then((res) => setResults(res.data.results || []))
        .catch(() => setResults([]))
        .finally(() => setIsLoading(false));
    }, 200);

    return () => clearTimeout(timer);
  }, [query]);

  if (!isOpen) return null;

  const handleSelect = (url: string) => {
    navigate(url);
    onClose();
  };

  const getIcon = (type: string) => {
    switch (type) {
      case "contact": return <User className="w-4 h-4 text-blue-500" />;
      case "company": return <Building2 className="w-4 h-4 text-purple-500" />;
      case "lead": return <Target className="w-4 h-4 text-emerald-500" />;
      case "deal": return <DollarSign className="w-4 h-4 text-amber-500" />;
      case "ticket": return <LifeBuoy className="w-4 h-4 text-rose-500" />;
      default: return <Search className="w-4 h-4 text-gray-400" />;
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-20 bg-black/50 backdrop-blur-sm p-4">
      <div className="bg-white rounded-xl shadow-2xl w-full max-w-2xl overflow-hidden border border-gray-100 animate-in fade-in zoom-in-95 duration-150">
        <div className="flex items-center px-4 py-3 border-b border-gray-100">
          <Search className="w-5 h-5 text-gray-400 mr-3" />
          <input
            type="text"
            className="flex-1 text-base bg-transparent border-none outline-none placeholder:text-gray-400 text-gray-800"
            placeholder="Search contacts, companies, leads, deals, tickets... (Type to search)"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            autoFocus
          />
          <button onClick={onClose} className="p-1 text-gray-400 hover:text-gray-600 rounded-lg">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="max-h-96 overflow-y-auto p-2">
          {isLoading && (
            <div className="p-4 text-center text-sm text-gray-500">Searching across CRM records...</div>
          )}

          {!isLoading && results.length === 0 && query.trim() && (
            <div className="p-4 text-center text-sm text-gray-500">No records found for "{query}"</div>
          )}

          {!isLoading && results.length === 0 && !query.trim() && (
            <div className="p-4 text-center text-xs text-gray-400">Quick tip: Search by name, email, company domain, or deal value</div>
          )}

          {results.map((r) => (
            <div
              key={`${r.entity_type}-${r.id}`}
              onClick={() => handleSelect(r.url)}
              className="flex items-center justify-between p-3 rounded-lg hover:bg-gray-50 cursor-pointer group transition-colors"
            >
              <div className="flex items-center space-x-3">
                <div className="p-2 rounded-md bg-gray-50 border border-gray-100">{getIcon(r.entity_type)}</div>
                <div>
                  <div className="text-sm font-medium text-gray-800 group-hover:text-brand-600 flex items-center gap-2">
                    {r.title}
                    <span className="text-[10px] font-semibold uppercase tracking-wider px-1.5 py-0.5 rounded bg-gray-100 text-gray-600">
                      {r.entity_type}
                    </span>
                  </div>
                  {r.subtitle && <div className="text-xs text-gray-500">{r.subtitle}</div>}
                </div>
              </div>
              <ArrowRight className="w-4 h-4 text-gray-300 group-hover:text-brand-500 group-hover:translate-x-1 transition-all" />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
""")

    # 3. frontend/src/components/ai-assistant/AICopilotDrawer.tsx
    write_file("frontend/src/components/ai-assistant/AICopilotDrawer.tsx", """import React, { useState } from "react";
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
""")

    # 4. frontend/src/components/layout/Navbar.tsx
    write_file("frontend/src/components/layout/Navbar.tsx", """import React from "react";
import { Search, Sparkles, Bell, Building, LogOut, ChevronDown, User } from "lucide-react";
import { useAuth } from "../../context/AuthContext";

interface Props {
  onOpenSearch: () => void;
  onOpenAI: () => void;
}

export const Navbar: React.FC<Props> = ({ onOpenSearch, onOpenAI }) => {
  const { user, organization, logout } = useAuth();

  return (
    <header className="h-16 bg-white border-b border-gray-200/80 px-6 flex items-center justify-between sticky top-0 z-30 shadow-xs">
      {/* Search trigger */}
      <div className="flex items-center gap-4 flex-1 max-w-lg">
        <button
          onClick={onOpenSearch}
          className="w-full flex items-center justify-between px-3.5 py-2 text-xs text-gray-400 bg-gray-50 hover:bg-gray-100 border border-gray-200 rounded-lg transition-all"
        >
          <div className="flex items-center gap-2">
            <Search className="w-4 h-4 text-gray-400" />
            <span>Search anything in ClientFlow...</span>
          </div>
          <kbd className="px-1.5 py-0.5 text-[10px] font-semibold text-gray-500 bg-white border border-gray-200 rounded shadow-2xs">
            Ctrl + K
          </kbd>
        </button>
      </div>

      {/* Right actions */}
      <div className="flex items-center space-x-3">
        {/* AI Copilot trigger */}
        <button
          onClick={onOpenAI}
          className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-emerald-700 bg-emerald-50 hover:bg-emerald-100 border border-emerald-200/60 rounded-lg transition-all shadow-2xs"
        >
          <Sparkles className="w-3.5 h-3.5 text-emerald-600" />
          <span>AI Copilot</span>
        </button>

        {/* Organization tag */}
        {organization && (
          <div className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 text-xs font-medium text-gray-700 bg-gray-100 rounded-md border border-gray-200">
            <Building className="w-3.5 h-3.5 text-gray-500" />
            <span>{organization.name}</span>
          </div>
        )}

        {/* User profile & logout */}
        {user && (
          <div className="flex items-center gap-3 pl-2 border-l border-gray-200">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-full bg-brand-600 text-white flex items-center justify-center font-semibold text-xs shadow-2xs">
                {user.first_name[0]}{user.last_name[0]}
              </div>
              <div className="hidden md:block text-left">
                <div className="text-xs font-semibold text-gray-800">{user.first_name} {user.last_name}</div>
                <div className="text-[10px] text-gray-400">{user.email}</div>
              </div>
            </div>
            <button
              onClick={logout}
              title="Sign Out"
              className="p-1.5 text-gray-400 hover:text-rose-600 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        )}
      </div>
    </header>
  );
};
""")

    # 5. frontend/src/components/layout/Sidebar.tsx
    write_file("frontend/src/components/layout/Sidebar.tsx", """import React from "react";
import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Users,
  Building2,
  Target,
  Kanban,
  Clock,
  CheckSquare,
  Calendar,
  MessageSquare,
  FolderLock,
  Package,
  FileCheck,
  Receipt,
  FileSpreadsheet,
  LifeBuoy,
  HeartHandshake,
  Megaphone,
  Workflow,
  Settings,
  Zap,
} from "lucide-react";

interface NavItem {
  name: string;
  to: string;
  icon: React.ReactNode;
}

const navGroups = [
  {
    group: "Overview",
    items: [
      { name: "Executive Dashboard", to: "/dashboard", icon: <LayoutDashboard className="w-4 h-4" /> },
      { name: "Activity Timeline", to: "/activities", icon: <Clock className="w-4 h-4" /> },
    ],
  },
  {
    group: "Sales & CRM",
    items: [
      { name: "Leads & Scoring", to: "/leads", icon: <Target className="w-4 h-4" /> },
      { name: "Contacts", to: "/contacts", icon: <Users className="w-4 h-4" /> },
      { name: "Companies", to: "/companies", icon: <Building2 className="w-4 h-4" /> },
      { name: "Deals & Pipelines", to: "/deals", icon: <Kanban className="w-4 h-4" /> },
      { name: "Tasks", to: "/tasks", icon: <CheckSquare className="w-4 h-4" /> },
      { name: "Calendar", to: "/calendar", icon: <Calendar className="w-4 h-4" /> },
    ],
  },
  {
    group: "Quote to Cash",
    items: [
      { name: "Products Catalog", to: "/products", icon: <Package className="w-4 h-4" /> },
      { name: "Proposals", to: "/proposals", icon: <FileCheck className="w-4 h-4" /> },
      { name: "Quotes", to: "/quotes", icon: <FileSpreadsheet className="w-4 h-4" /> },
      { name: "Invoices", to: "/invoices", icon: <Receipt className="w-4 h-4" /> },
    ],
  },
  {
    group: "Customer Operations",
    items: [
      { name: "Support Tickets", to: "/support", icon: <LifeBuoy className="w-4 h-4" /> },
      { name: "Customer Success", to: "/customer-success", icon: <HeartHandshake className="w-4 h-4" /> },
      { name: "Communications", to: "/communications", icon: <MessageSquare className="w-4 h-4" /> },
      { name: "Documents Vault", to: "/documents", icon: <FolderLock className="w-4 h-4" /> },
    ],
  },
  {
    group: "Growth & Engine",
    items: [
      { name: "Campaigns", to: "/campaigns", icon: <Megaphone className="w-4 h-4" /> },
      { name: "Automations", to: "/automations", icon: <Workflow className="w-4 h-4" /> },
      { name: "Settings", to: "/settings", icon: <Settings className="w-4 h-4" /> },
    ],
  },
];

export const Sidebar: React.FC = () => {
  return (
    <aside className="w-64 bg-slate-900 text-slate-300 flex flex-col h-screen sticky top-0 select-none border-r border-slate-800">
      {/* Brand Header */}
      <div className="h-16 px-6 flex items-center gap-3 border-b border-slate-800/80 bg-slate-950/40">
        <div className="w-8 h-8 rounded-lg bg-emerald-500 text-slate-950 flex items-center justify-center font-bold shadow-md shadow-emerald-500/20">
          <Zap className="w-5 h-5 fill-current" />
        </div>
        <div>
          <span className="font-bold text-sm text-white tracking-tight">ClientFlow</span>
          <span className="text-[10px] block text-emerald-400 font-semibold uppercase tracking-widest -mt-1">Enterprise CRM</span>
        </div>
      </div>

      {/* Navigation Groups */}
      <div className="flex-1 overflow-y-auto px-3 py-4 space-y-6">
        {navGroups.map((group, gIdx) => (
          <div key={gIdx} className="space-y-1">
            <div className="px-3 text-[10px] font-semibold uppercase tracking-wider text-slate-500">{group.group}</div>
            {group.items.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-medium transition-all ${
                    isActive
                      ? "bg-emerald-500/10 text-emerald-400 font-semibold shadow-2xs border border-emerald-500/20"
                      : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
                  }`
                }
              >
                {item.icon}
                <span>{item.name}</span>
              </NavLink>
            ))}
          </div>
        ))}
      </div>
    </aside>
  );
};
""")

    # 6. frontend/src/components/layout/AppLayout.tsx
    write_file("frontend/src/components/layout/AppLayout.tsx", """import React, { useState } from "react";
import { Outlet } from "react-router-dom";
import { Sidebar } from "./Sidebar";
import { Navbar } from "./Navbar";
import { GlobalSearchModal } from "../common/GlobalSearchModal";
import { AICopilotDrawer } from "../ai-assistant/AICopilotDrawer";

export const AppLayout: React.FC = () => {
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [isAIOpen, setIsAIOpen] = useState(false);

  // Keyboard shortcut Ctrl+K
  React.useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "k") {
        e.preventDefault();
        setIsSearchOpen((prev) => !prev);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  return (
    <div className="flex min-h-screen bg-slate-50">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <Navbar onOpenSearch={() => setIsSearchOpen(true)} onOpenAI={() => setIsAIOpen(true)} />
        <main className="flex-1 p-6 md:p-8 max-w-7xl w-full mx-auto">
          <Outlet />
        </main>
      </div>

      <GlobalSearchModal isOpen={isSearchOpen} onClose={() => setIsSearchOpen(false)} />
      <AICopilotDrawer isOpen={isAIOpen} onClose={() => setIsAIOpen(false)} />
    </div>
  );
};
""")

    print("Frontend Layout, Search & AI Copilot generated.")

if __name__ == '__main__':
    run()
