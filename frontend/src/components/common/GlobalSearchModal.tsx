import React, { useState, useEffect } from "react";
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
