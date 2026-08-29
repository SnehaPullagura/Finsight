import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    write_file("frontend/src/pages/support/SupportPage.tsx", """import React, { useEffect, useState } from "react";
import { LifeBuoy, AlertCircle, CheckCircle2 } from "lucide-react";
import { api } from "../../services/api";
import { Ticket } from "../../types";

export const SupportPage: React.FC = () => {
  const [tickets, setTickets] = useState<Ticket[]>([]);

  useEffect(() => {
    api.getTickets().then(res => setTickets(res.data)).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-900">Customer Support & SLA</h1>
        <p className="text-xs text-slate-500">Omnichannel tickets, SLA breach prevention, and resolution queues</p>
      </div>

      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-2xs">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-50 text-slate-600 font-semibold border-b">
            <tr>
              <th className="p-3.5">Ticket #</th>
              <th className="p-3.5">Subject</th>
              <th className="p-3.5">Priority</th>
              <th className="p-3.5">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-slate-700">
            {tickets.map(t => (
              <tr key={t.id} className="hover:bg-slate-50">
                <td className="p-3.5 font-semibold text-slate-900">{t.ticket_number}</td>
                <td className="p-3.5">{t.subject}</td>
                <td className="p-3.5">
                  <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${t.priority === 'urgent' ? 'bg-rose-100 text-rose-800' : 'bg-slate-100 text-slate-700'}`}>
                    {t.priority}
                  </span>
                </td>
                <td className="p-3.5">
                  <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-100 text-emerald-800 uppercase">{t.status}</span>
                </td>
              </tr>
            ))}
            {tickets.length === 0 && <tr><td colSpan={4} className="p-8 text-center text-slate-400">No support tickets in queue.</td></tr>}
          </tbody>
        </table>
      </div>
    </div>
  );
};
""")

    write_file("frontend/src/pages/customer-success/CustomerSuccessPage.tsx", """import React, { useEffect, useState } from "react";
import { HeartHandshake, ShieldAlert, CheckCircle2 } from "lucide-react";
import { api } from "../../services/api";
import { CustomerSuccessPlan } from "../../types";

export const CustomerSuccessPage: React.FC = () => {
  const [plans, setPlans] = useState<CustomerSuccessPlan[]>([]);

  useEffect(() => {
    api.getSuccessPlans().then(res => setPlans(res.data)).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-900">Customer Success & Health</h1>
        <p className="text-xs text-slate-500">Client health scores, onboarding tracks, and churn risk mitigation</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {plans.map(p => (
          <div key={p.id} className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-xs font-bold text-slate-900">Health Score: {p.health_score}/100</span>
              <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold uppercase ${p.health_grade === 'good' ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'}`}>
                {p.health_grade}
              </span>
            </div>
            <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
              <div className={`h-full ${p.health_score > 70 ? 'bg-emerald-500' : 'bg-amber-500'} rounded-full`} style={{ width: `${p.health_score}%` }}></div>
            </div>
            <div className="text-[11px] text-slate-500">Milestones: {p.milestones?.length || 0} tracks configured</div>
          </div>
        ))}
        {plans.length === 0 && <div className="p-8 col-span-full text-center text-xs text-slate-400 bg-white rounded-xl border border-slate-200">Customer success plans active.</div>}
      </div>
    </div>
  );
};
""")

    write_file("frontend/src/pages/campaigns/CampaignsPage.tsx", """import React, { useEffect, useState } from "react";
import { Megaphone, Play } from "lucide-react";
import { api } from "../../services/api";
import { Campaign } from "../../types";

export const CampaignsPage: React.FC = () => {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);

  useEffect(() => {
    api.getCampaigns().then(res => setCampaigns(res.data)).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-900">Marketing Campaigns</h1>
        <p className="text-xs text-slate-500">Audience segmentation, email/SMS broadcasts, and attribution</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {campaigns.map(c => (
          <div key={c.id} className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs space-y-2">
            <h4 className="text-xs font-bold text-slate-900">{c.name}</h4>
            <div className="text-[11px] text-slate-500">{c.sent_count} sent • {c.open_count} opened • {c.conversion_count} converted</div>
          </div>
        ))}
        {campaigns.length === 0 && <div className="p-8 col-span-full text-center text-xs text-slate-400 bg-white rounded-xl border border-slate-200">No campaigns launched.</div>}
      </div>
    </div>
  );
};
""")

    write_file("frontend/src/pages/automations/AutomationsPage.tsx", """import React, { useEffect, useState } from "react";
import { Workflow, PlayCircle } from "lucide-react";
import { api } from "../../services/api";
import { AutomationWorkflow } from "../../types";

export const AutomationsPage: React.FC = () => {
  const [workflows, setWorkflows] = useState<AutomationWorkflow[]>([]);

  useEffect(() => {
    api.getWorkflows().then(res => setWorkflows(res.data)).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-900">Workflow Automation Engine</h1>
        <p className="text-xs text-slate-500">Event-driven triggers, conditional logic trees, and automated task actions</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {workflows.map(w => (
          <div key={w.id} className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs space-y-3">
            <div className="flex justify-between items-start">
              <h4 className="text-xs font-bold text-slate-900">{w.name}</h4>
              <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-100 text-emerald-800">Active</span>
            </div>
            <div className="text-xs text-slate-600 bg-slate-50 p-2.5 rounded border border-slate-100 font-mono text-[11px]">
              When: {w.trigger_event} ➔ Then: {w.actions.length} Actions
            </div>
          </div>
        ))}
        {workflows.length === 0 && <div className="p-8 col-span-full text-center text-xs text-slate-400 bg-white rounded-xl border border-slate-200">Workflows active in background engine.</div>}
      </div>
    </div>
  );
};
""")

    write_file("frontend/src/pages/settings/SettingsPage.tsx", """import React from "react";
import { Settings, Shield, Users, Sliders } from "lucide-react";
import { useAuth } from "../../context/AuthContext";

export const SettingsPage: React.FC = () => {
  const { organization, user } = useAuth();

  return (
    <div className="space-y-6 max-w-4xl">
      <div>
        <h1 className="text-xl font-bold text-slate-900">Organization Settings</h1>
        <p className="text-xs text-slate-500">Workspace preferences, RBAC access control, and security</p>
      </div>

      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-2xs space-y-4">
        <h3 className="text-xs font-bold text-slate-900">Tenant Profile</h3>
        <div className="grid grid-cols-2 gap-4 text-xs">
          <div>
            <label className="text-slate-400 block mb-1">Organization Name</label>
            <input disabled className="w-full bg-slate-50 border p-2 rounded text-slate-700" value={organization?.name || "Apex Global"} />
          </div>
          <div>
            <label className="text-slate-400 block mb-1">Plan Tier</label>
            <input disabled className="w-full bg-slate-50 border p-2 rounded text-slate-700 uppercase font-semibold text-emerald-600" value={organization?.plan_tier || "Enterprise"} />
          </div>
        </div>
      </div>
    </div>
  );
};
""")

    # App.tsx
    write_file("frontend/src/App.tsx", """import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import { AppLayout } from "./components/layout/AppLayout";
import { LoginPage } from "./pages/auth/LoginPage";
import { RegisterPage } from "./pages/auth/RegisterPage";
import { DashboardPage } from "./pages/dashboard/DashboardPage";
import { ContactsPage } from "./pages/contacts/ContactsPage";
import { CompaniesPage } from "./pages/companies/CompaniesPage";
import { LeadsPage } from "./pages/leads/LeadsPage";
import { DealsKanbanPage } from "./pages/deals/DealsKanbanPage";
import { TimelinePage } from "./pages/activities/TimelinePage";
import { TasksPage } from "./pages/tasks/TasksPage";
import { CalendarPage } from "./pages/calendar/CalendarPage";
import { CommunicationsPage } from "./pages/communications/CommunicationsPage";
import { DocumentsPage } from "./pages/documents/DocumentsPage";
import { ProductsPage } from "./pages/products/ProductsPage";
import { ProposalsPage } from "./pages/proposals/ProposalsPage";
import { QuotesPage } from "./pages/quotes/QuotesPage";
import { InvoicesPage } from "./pages/invoices/InvoicesPage";
import { SupportPage } from "./pages/support/SupportPage";
import { CustomerSuccessPage } from "./pages/customer-success/CustomerSuccessPage";
import { CampaignsPage } from "./pages/campaigns/CampaignsPage";
import { AutomationsPage } from "./pages/automations/AutomationsPage";
import { SettingsPage } from "./pages/settings/SettingsPage";

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();
  if (isLoading) return <div className="h-screen flex items-center justify-center text-xs text-slate-500">Loading ClientFlow CRM...</div>;
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return <>{children}</>;
};

export const App: React.FC = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          
          <Route path="/" element={<ProtectedRoute><AppLayout /></ProtectedRoute>}>
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard" element={<DashboardPage />} />
            <Route path="contacts" element={<ContactsPage />} />
            <Route path="companies" element={<CompaniesPage />} />
            <Route path="leads" element={<LeadsPage />} />
            <Route path="deals" element={<DealsKanbanPage />} />
            <Route path="activities" element={<TimelinePage />} />
            <Route path="tasks" element={<TasksPage />} />
            <Route path="calendar" element={<CalendarPage />} />
            <Route path="communications" element={<CommunicationsPage />} />
            <Route path="documents" element={<DocumentsPage />} />
            <Route path="products" element={<ProductsPage />} />
            <Route path="proposals" element={<ProposalsPage />} />
            <Route path="quotes" element={<QuotesPage />} />
            <Route path="invoices" element={<InvoicesPage />} />
            <Route path="support" element={<SupportPage />} />
            <Route path="customer-success" element={<CustomerSuccessPage />} />
            <Route path="campaigns" element={<CampaignsPage />} />
            <Route path="automations" element={<AutomationsPage />} />
            <Route path="settings" element={<SettingsPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};
export default App;
""")

    # main.tsx
    write_file("frontend/src/main.tsx", """import React from "react";
import ReactDOM from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import App from "./App";
import "./index.css";

const queryClient = new QueryClient();

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </React.StrictMode>
);
""")

    print("Frontend Part D2 (Support, Success, Campaigns, Automations, Settings, App.tsx, main.tsx) generated.")

if __name__ == '__main__':
    run()
