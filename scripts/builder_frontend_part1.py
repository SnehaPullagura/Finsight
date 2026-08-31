import os
import sys
from scripts.common import write_file

def build_frontend():
    print("Building Phase 7: Modern React 18 + TypeScript + Vite + Tailwind CSS SPA...")

    # 1. Package Configuration
    write_file("frontend/package.json", """{
  "name": "finsight-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0"
  },
  "dependencies": {
    "clsx": "^2.1.1",
    "lucide-react": "^0.395.0",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-router-dom": "^6.23.1",
    "tailwind-merge": "^2.3.0"
  },
  "devDependencies": {
    "@types/node": "^20.14.2",
    "@types/react": "^18.3.3",
    "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.3.0",
    "autoprefixer": "^10.4.19",
    "postcss": "^8.4.38",
    "tailwindcss": "^3.4.4",
    "typescript": "^5.4.5",
    "vite": "^5.2.13"
  }
}
""")

    write_file("frontend/tsconfig.json", """{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": false,
    "noUnusedLocals": false,
    "noUnusedParameters": false,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"]
}
""")

    write_file("frontend/tsconfig.node.json", """{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}
""")

    write_file("frontend/vite.config.ts", """import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: false
  }
});
""")

    write_file("frontend/tailwind.config.js", """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eef2ff',
          100: '#e0e7ff',
          500: '#6366f1',
          600: '#4f46e5',
          700: '#4338ca',
          800: '#3730a3',
          900: '#312e81',
        }
      }
    },
  },
  plugins: [],
}
""")

    write_file("frontend/postcss.config.js", """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
""")

    write_file("frontend/index.html", """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>FinSight — AI-Powered Financial Health & Cash-Flow Intelligence</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  </head>
  <body class="bg-slate-950 text-slate-100 font-sans antialiased min-h-screen selection:bg-indigo-500 selection:text-white">
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
""")

    write_file("frontend/src/index.css", """@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  font-family: 'Inter', sans-serif;
  margin: 0;
  background-color: #030712;
  color: #f8fafc;
}

.mono {
  font-family: 'JetBrains Mono', monospace;
}

/* Glassmorphism utility classes */
.glass-panel {
  background: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(51, 65, 85, 0.5);
}

.glass-card {
  background: rgba(30, 41, 59, 0.6);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(51, 65, 85, 0.4);
}

.glass-dropdown {
  background: rgba(15, 23, 42, 0.95);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(71, 85, 105, 0.6);
}

/* Custom Scrollbar */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: #090d16;
}
::-webkit-scrollbar-thumb {
  background: #334155;
  border-radius: 9999px;
}
::-webkit-scrollbar-thumb:hover {
  background: #475569;
}
""")

    # 2. TypeScript Types & API Client
    write_file("frontend/src/types/index.ts", """
export interface User {
  id: number;
  email: string;
  full_name: string;
  role: string;
  preferred_currency: string;
  is_active: boolean;
  created_at: string;
}

export interface FinancialAccount {
  id: number;
  name: string;
  account_type: string;
  account_number_masked: string;
  institution_name: string;
  currency: string;
  current_balance: number;
  available_balance: number;
  credit_limit?: number;
  interest_rate?: number;
  status: string;
  is_primary: boolean;
  last_reconciled_at?: string;
  notes?: string;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  group: string;
  icon: string;
  color: string;
}

export interface Transaction {
  id: number;
  account_id: number;
  category_id?: number;
  amount: number;
  transaction_type: 'income' | 'expense' | 'transfer' | 'refund' | 'fee' | 'interest';
  transaction_date: string;
  description: string;
  merchant_name?: string;
  status: string;
  is_recurring: boolean;
  is_discretionary: boolean;
  confidence_score: number;
  category?: Category;
}

export interface BudgetProgress {
  id: number;
  name: string;
  allocated_amount: number;
  spent_amount: number;
  remaining_amount: number;
  percentage_used: number;
  is_overbudget: boolean;
  status: 'good' | 'warning' | 'exceeded';
  category?: Category;
}

export interface FinancialGoal {
  id: number;
  name: string;
  goal_type: string;
  target_amount: number;
  current_amount: number;
  target_date: string;
  monthly_contribution: number;
  percentage_completed: number;
  projected_completion_date?: string;
  sufficiency_status: 'on_track' | 'behind' | 'ahead';
  notes?: string;
}

export interface RecurringPayment {
  id: number;
  merchant_name: string;
  amount: number;
  cadence: string;
  next_expected_date: string;
  last_payment_date?: string;
  is_active: boolean;
  category?: Category;
}

export interface CashFlowPoint {
  date: string;
  cash_in: number;
  cash_out: number;
  net_cash_flow: number;
  projected_balance: number;
}

export interface CashFlowSummary {
  total_cash_in: number;
  total_cash_out: number;
  net_cash_flow: number;
  savings_rate_percent: number;
  average_daily_burn_rate: number;
  liquidity_runway_days: number;
  daily_timeline: CashFlowPoint[];
  category_cash_out_breakdown: Record<string, number>;
}

export interface HealthPillar {
  pillar_name: string;
  score: number;
  weight: number;
  status: 'strong' | 'moderate' | 'weak';
  metric_value: string;
  description: string;
}

export interface FinancialHealth {
  overall_score: number;
  grade: string;
  score_change_mom: number;
  explanation: string;
  pillars: HealthPillar[];
  strengths: string[];
  attention_areas: string[];
  recommended_actions: string[];
}

export interface Scenario {
  id: number;
  name: string;
  description?: string;
  monthly_income_delta: number;
  monthly_expense_delta: number;
  one_time_lump_sum: number;
  loan_amount: number;
  calculated_monthly_emi: number;
  projected_6m_balance: number;
  projected_12m_balance: number;
  health_score_delta: number;
  is_feasible: boolean;
  feasibility_notes?: string;
}

export interface Anomaly {
  id: number;
  transaction_id: number;
  anomaly_type: string;
  anomaly_score: number;
  severity: string;
  explanation: string;
  is_acknowledged: boolean;
  transaction?: Transaction;
  created_at: string;
}

export interface ForecastResponse {
  horizon_days: number;
  predicted_total_income: number;
  predicted_total_expenses: number;
  predicted_net_savings: number;
  current_balance: number;
  projected_ending_balance: number;
  shortage_risk_probability: number;
  risk_level: string;
  savings_trajectory: Record<string, number>;
  daily_projections: Array<{
    date: string;
    predicted_balance: number;
    lower_bound: number;
    upper_bound: number;
  }>;
}

export interface AnalyticsOverview {
  mom: {
    current_month: string;
    previous_month: string;
    income_current: number;
    income_previous: number;
    income_growth_percent: number;
    expense_current: number;
    expense_previous: number;
    expense_growth_percent: number;
    savings_rate_current: number;
  };
  velocity: {
    daily_burn_rate: number;
    projected_month_end_expense: number;
    days_elapsed: number;
    days_remaining: number;
    pace_status: string;
  };
  financial_stability_index: number;
  recurring_expense_ratio: number;
  discretionary_ratio: number;
  top_merchants: Array<{ merchant: string; amount: number }>;
}

export interface NotificationItem {
  id: number;
  notification_type: string;
  title: string;
  message: string;
  is_read: boolean;
  action_url?: string;
  created_at: string;
}
""")

    write_file("frontend/src/services/api.ts", """
const API_BASE = '/api/v1';

function getHeaders(): HeadersInit {
  const token = localStorage.getItem('finsight_token');
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {})
  };
}

export async function apiRequest<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      ...getHeaders(),
      ...(options.headers || {})
    }
  });

  if (response.status === 401) {
    localStorage.removeItem('finsight_token');
    localStorage.removeItem('finsight_user');
    if (!window.location.pathname.includes('/login')) {
      window.location.href = '/login';
    }
    throw new Error('Unauthorized');
  }

  if (!response.ok) {
    const errData = await response.json().catch(() => ({}));
    throw new Error(errData.message || `API Error: ${response.statusText}`);
  }

  return response.json();
}

export const api = {
  // Auth
  login: (data: any) => apiRequest<any>('/auth/login', { method: 'POST', body: JSON.stringify(data) }),
  register: (data: any) => apiRequest<any>('/auth/register', { method: 'POST', body: JSON.stringify(data) }),
  getMe: () => apiRequest<any>('/auth/me'),
  logout: () => apiRequest<any>('/auth/logout', { method: 'POST' }),

  // Accounts
  getAccounts: () => apiRequest<any[]>('/accounts'),
  createAccount: (data: any) => apiRequest<any>('/accounts', { method: 'POST', body: JSON.stringify(data) }),
  reconcileAccount: (id: number, data: any) => apiRequest<any>(`/accounts/${id}/reconcile`, { method: 'POST', body: JSON.stringify(data) }),

  // Categories
  getCategories: () => apiRequest<any[]>('/categories'),

  // Transactions
  getTransactions: (params: string = '') => apiRequest<any[]>(`/transactions${params}`),
  createTransaction: (data: any) => apiRequest<any>('/transactions', { method: 'POST', body: JSON.stringify(data) }),
  deleteTransaction: (id: number) => apiRequest<any>(`/transactions/${id}`, { method: 'DELETE' }),

  // Budgets
  getBudgets: () => apiRequest<any[]>('/budgets'),
  createBudget: (data: any) => apiRequest<any>('/budgets', { method: 'POST', body: JSON.stringify(data) }),

  // Goals
  getGoals: () => apiRequest<any[]>('/goals'),
  createGoal: (data: any) => apiRequest<any>('/goals', { method: 'POST', body: JSON.stringify(data) }),
  contributeGoal: (id: number, data: any) => apiRequest<any>(`/goals/${id}/contribute`, { method: 'POST', body: JSON.stringify(data) }),

  // Recurring
  getRecurring: () => apiRequest<any[]>('/recurring'),
  detectRecurring: () => apiRequest<any[]>('/recurring/detect', { method: 'POST' }),
  getCalendar: () => apiRequest<any[]>('/recurring/calendar'),

  // Cashflow & Health
  getCashFlowSummary: () => apiRequest<any>('/cashflow/summary'),
  getHealthScore: () => apiRequest<any>('/health/score'),

  // Forecasts & Analytics
  getForecast: (days: number = 30) => apiRequest<any>(`/forecasts/expenses?horizon_days=${days}`),
  getAnalytics: () => apiRequest<any>('/analytics/overview'),

  // Scenarios
  getScenariosCompare: () => apiRequest<any>('/scenarios/compare'),
  createScenario: (data: any) => apiRequest<any>('/scenarios', { method: 'POST', body: JSON.stringify(data) }),

  // AI Assistant
  queryAssistant: (query: string) => apiRequest<any>('/assistant/query', { method: 'POST', body: JSON.stringify({ query }) }),

  // Anomalies
  getAnomalies: () => apiRequest<any[]>('/anomalies'),
  acknowledgeAnomaly: (id: number, data: any) => apiRequest<any>(`/anomalies/${id}/acknowledge`, { method: 'POST', body: JSON.stringify(data) }),

  // Notifications
  getNotifications: () => apiRequest<any[]>('/notifications'),
  markNotificationRead: (id: number) => apiRequest<any>(`/notifications/${id}/read`, { method: 'PATCH' }),
  markAllNotificationsRead: () => apiRequest<any>('/notifications/read-all', { method: 'POST' }),

  // Reports & Admin
  generateReport: (data: any) => apiRequest<any>('/reports/generate', { method: 'POST', body: JSON.stringify(data) }),
  getAdminMetrics: () => apiRequest<any>('/admin/metrics'),
  getMLModels: () => apiRequest<any[]>('/admin/models')
};
""")

    write_file("frontend/src/context/AuthContext.tsx", """
import React, { createContext, useContext, useState, useEffect } from 'react';
import { User } from '../types';
import { api } from '../services/api';

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (email: string, pass: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType>({} as AuthContextType);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(() => {
    const saved = localStorage.getItem('finsight_user');
    return saved ? JSON.parse(saved) : null;
  });
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('finsight_token'));
  const [loading, setLoading] = useState(false);

  const login = async (email: string, pass: string) => {
    setLoading(true);
    try {
      const res = await api.login({ email, password: pass });
      localStorage.setItem('finsight_token', res.access_token);
      localStorage.setItem('finsight_user', JSON.stringify(res.user));
      setToken(res.access_token);
      setUser(res.user);
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('finsight_token');
    localStorage.removeItem('finsight_user');
    setUser(null);
    setToken(null);
    window.location.href = '/login';
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
""")

    print("Phase 7 base frontend configuration created!")

if __name__ == "__main__":
    build_frontend()
