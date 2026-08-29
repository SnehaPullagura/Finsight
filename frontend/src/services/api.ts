import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("clientflow_access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  const tenantId = localStorage.getItem("clientflow_tenant_id");
  if (tenantId) {
    config.headers["X-Tenant-ID"] = tenantId;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401 && !error.config._retry) {
      error.config._retry = true;
      const refreshToken = localStorage.getItem("clientflow_refresh_token");
      if (refreshToken) {
        try {
          const res = await axios.post(`${API_BASE_URL}/auth/refresh`, { refresh_token: refreshToken });
          localStorage.setItem("clientflow_access_token", res.data.access_token);
          error.config.headers.Authorization = `Bearer ${res.data.access_token}`;
          return apiClient(error.config);
        } catch (refreshErr) {
          localStorage.removeItem("clientflow_access_token");
          localStorage.removeItem("clientflow_refresh_token");
          window.location.href = "/login";
        }
      }
    }
    return Promise.reject(error);
  }
);

export const api = {
  // Auth
  login: (data: any) => apiClient.post("/auth/login", data),
  register: (data: any) => apiClient.post("/auth/register", data),
  getMe: () => apiClient.get("/auth/me"),
  setupMfa: () => apiClient.post("/auth/mfa/setup"),
  verifyMfa: (code: string) => apiClient.post("/auth/mfa/verify", { code }),

  // Organizations
  getCurrentOrg: () => apiClient.get("/organizations/current"),
  createOrg: (data: any) => apiClient.post("/organizations", data),
  getOrgMembers: () => apiClient.get("/organizations/members"),
  inviteMember: (data: any) => apiClient.post("/organizations/invitations", data),

  // Contacts & Companies
  getContacts: (params?: any) => apiClient.get("/contacts", { params }),
  getContact: (id: string) => apiClient.get(`/contacts/${id}`),
  createContact: (data: any) => apiClient.post("/contacts", data),
  updateContact: (id: string, data: any) => apiClient.put(`/contacts/${id}`, data),
  deleteContact: (id: string) => apiClient.delete(`/contacts/${id}`),
  checkDuplicates: (params: any) => apiClient.get("/contacts/deduplicate", { params }),

  getCompanies: (params?: any) => apiClient.get("/companies", { params }),
  getCompany: (id: string) => apiClient.get(`/companies/${id}`),
  createCompany: (data: any) => apiClient.post("/companies", data),
  updateCompany: (id: string, data: any) => apiClient.put(`/companies/${id}`, data),
  deleteCompany: (id: string) => apiClient.delete(`/companies/${id}`),

  // Leads
  getLeads: (params?: any) => apiClient.get("/leads", { params }),
  getLead: (id: string) => apiClient.get(`/leads/${id}`),
  createLead: (data: any) => apiClient.post("/leads", data),
  updateLead: (id: string, data: any) => apiClient.put(`/leads/${id}`, data),
  deleteLead: (id: string) => apiClient.delete(`/leads/${id}`),
  qualifyLead: (id: string) => apiClient.post(`/leads/${id}/qualify`),
  convertLead: (id: string, data: any) => apiClient.post(`/leads/${id}/convert`, data),

  // Deals & Pipelines
  getPipelines: () => apiClient.get("/pipelines"),
  createPipeline: (data: any) => apiClient.post("/pipelines", data),
  getDeals: (params?: any) => apiClient.get("/deals", { params }),
  getKanbanBoard: (pipelineId?: string) => apiClient.get("/deals/kanban", { params: { pipeline_id: pipelineId } }),
  createDeal: (data: any) => apiClient.post("/deals", data),
  updateDeal: (id: string, data: any) => apiClient.put(`/deals/${id}`, data),
  transitionDealStage: (id: string, data: any) => apiClient.post(`/deals/${id}/stage`, data),

  // Activities & Tasks & Calendar
  getTimeline: (entityType: string, entityId: string) => apiClient.get(`/activities/timeline/${entityType}/${entityId}`),
  createActivity: (data: any) => apiClient.post("/activities", data),
  getTasks: (params?: any) => apiClient.get("/tasks", { params }),
  createTask: (data: any) => apiClient.post("/tasks", data),
  completeTask: (id: string) => apiClient.post(`/tasks/${id}/complete`),
  getCalendarEvents: (params?: any) => apiClient.get("/calendar/events", { params }),
  createCalendarEvent: (data: any) => apiClient.post("/calendar/events", data),

  // Products, Proposals, Quotes & Invoices
  getProducts: () => apiClient.get("/products"),
  createProduct: (data: any) => apiClient.post("/products", data),
  getProposals: () => apiClient.get("/proposals"),
  createProposal: (data: any) => apiClient.post("/proposals", data),
  acceptProposal: (id: string) => apiClient.post(`/proposals/${id}/accept`),
  getQuotes: () => apiClient.get("/quotes"),
  createQuote: (data: any) => apiClient.post("/quotes", data),
  getInvoices: () => apiClient.get("/invoices"),
  createInvoice: (data: any) => apiClient.post("/invoices", data),
  recordPayment: (id: string, data: any) => apiClient.post(`/invoices/${id}/payments`, data),

  // Support & Customer Success
  getTickets: (params?: any) => apiClient.get("/support/tickets", { params }),
  createTicket: (data: any) => apiClient.post("/support/tickets", data),
  resolveTicket: (id: string, data: any) => apiClient.post(`/support/tickets/${id}/resolve`, data),
  getSuccessPlans: () => apiClient.get("/customer-success/plans"),
  createSuccessPlan: (data: any) => apiClient.post("/customer-success/plans", data),
  recalculateHealth: (id: string) => apiClient.post(`/customer-success/plans/${id}/recalculate-health`),

  // Campaigns & Automations
  getCampaigns: () => apiClient.get("/campaigns"),
  createCampaign: (data: any) => apiClient.post("/campaigns", data),
  launchCampaign: (id: string) => apiClient.post(`/campaigns/${id}/launch`),
  getWorkflows: () => apiClient.get("/automations"),
  createWorkflow: (data: any) => apiClient.post("/automations", data),

  // Global Search & Analytics & AI
  globalSearch: (q: string) => apiClient.get("/search", { params: { q } }),
  getDashboardAnalytics: () => apiClient.get("/analytics/dashboard"),
  summarizeLeadAI: (id: string) => apiClient.post(`/ai/summarize/lead/${id}`),
  analyzeDealRiskAI: (id: string) => apiClient.post(`/ai/analyze/deal/${id}`),
  draftEmailAI: (data: any) => apiClient.post("/ai/draft/email", data),
  nlQueryAI: (data: any) => apiClient.post("/ai/query", data),
};
