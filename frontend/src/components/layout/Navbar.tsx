import React from "react";
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
