import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { AppLayout } from './components/layout/AppLayout';
import { LoginPage } from './pages/auth/LoginPage';
import { DashboardPage } from './pages/dashboard/DashboardPage';
import { ScenarioSimulatorPage } from './pages/scenarios/ScenarioSimulatorPage';
import { AssistantPage } from './pages/assistant/AssistantPage';
import { AccountsPage } from './pages/accounts/AccountsPage';
import { TransactionsPage } from './pages/transactions/TransactionsPage';
import { BudgetsPage } from './pages/budgets/BudgetsPage';
import { GoalsPage } from './pages/goals/GoalsPage';
import { DataImportPage } from './pages/imports/DataImportPage';
import { AdminPage } from './pages/admin/AdminPage';

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user } = useAuth();
  if (!user && !localStorage.getItem('finsight_token')) {
    return <Navigate to="/login" replace />;
  }
  return <>{children}</>;
};

export const App: React.FC = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/" element={<ProtectedRoute><AppLayout /></ProtectedRoute>}>
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard" element={<DashboardPage />} />
            <Route path="health" element={<DashboardPage />} />
            <Route path="cashflow" element={<DashboardPage />} />
            <Route path="scenarios" element={<ScenarioSimulatorPage />} />
            <Route path="assistant" element={<AssistantPage />} />
            <Route path="accounts" element={<AccountsPage />} />
            <Route path="transactions" element={<TransactionsPage />} />
            <Route path="budgets" element={<BudgetsPage />} />
            <Route path="goals" element={<GoalsPage />} />
            <Route path="recurring" element={<DashboardPage />} />
            <Route path="forecasts" element={<DashboardPage />} />
            <Route path="analytics" element={<DashboardPage />} />
            <Route path="anomalies" element={<DashboardPage />} />
            <Route path="imports" element={<DataImportPage />} />
            <Route path="reports" element={<DashboardPage />} />
            <Route path="admin" element={<AdminPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};
