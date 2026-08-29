import React from "react";
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
