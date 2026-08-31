import { CPQPage } from "./pages/cpq/CPQPage";
import { AdvancedAnalyticsPage } from "./pages/analytics/AdvancedAnalyticsPage";
import { IntegrationsPage } from "./pages/integrations/IntegrationsPage";
import { GovernancePage } from "./pages/governance/GovernancePage";
import React from "react";
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
            <Route path="cpq" element={<CPQPage />} />
            <Route path="advanced-analytics" element={<AdvancedAnalyticsPage />} />
            <Route path="integrations" element={<IntegrationsPage />} />
            <Route path="governance" element={<GovernancePage />} />
            <Route path="settings" element={<SettingsPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};
export default App;
