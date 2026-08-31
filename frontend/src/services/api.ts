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
