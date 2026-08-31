import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. frontend/src/types/index.ts
    write_file("frontend/src/types/index.ts", """export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  phone?: string;
  avatar_url?: string;
  is_active: boolean;
  is_verified: boolean;
  is_superuser: boolean;
  mfa_enabled: boolean;
  created_at: string;
  roles: string[];
}

export interface Organization {
  id: string;
  name: string;
  slug: string;
  domain?: string;
  plan_tier: string;
  is_active: boolean;
  logo_url?: string;
  settings: Record<string, any>;
  created_at: string;
}

export interface Contact {
  id: string;
  tenant_id: string;
  first_name: string;
  last_name: string;
  email: string;
  secondary_email?: string;
  phone?: string;
  mobile_phone?: string;
  title?: string;
  department?: string;
  company_id?: string;
  owner_id?: string;
  lifecycle_stage: string;
  lead_source?: string;
  city?: string;
  state?: string;
  country?: string;
  linkedin_url?: string;
  is_do_not_call: boolean;
  is_do_not_email: boolean;
  custom_fields: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface Company {
  id: string;
  tenant_id: string;
  name: string;
  legal_name?: string;
  domain?: string;
  website?: string;
  industry?: string;
  annual_revenue?: number;
  currency: string;
  employee_count?: number;
  parent_company_id?: string;
  owner_id?: string;
  phone?: string;
  city?: string;
  state?: string;
  country?: string;
  linkedin_url?: string;
  description?: string;
  custom_fields: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface Lead {
  id: string;
  tenant_id: string;
  first_name: string;
  last_name: string;
  email: string;
  phone?: string;
  company_name?: string;
  title?: string;
  status: string;
  source: string;
  score: number;
  qualification_grade: string;
  qualification_details: Record<string, any>;
  estimated_budget?: number;
  employee_count?: number;
  industry?: string;
  intent_score: number;
  engagement_count: number;
  owner_id?: string;
  converted_at?: string;
  converted_contact_id?: string;
  converted_company_id?: string;
  converted_deal_id?: string;
  notes?: string;
  custom_fields: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface PipelineStage {
  id: string;
  pipeline_id: string;
  name: string;
  stage_order: number;
  probability: number;
  stage_type: string;
  sla_days?: number;
  created_at: string;
}

export interface Pipeline {
  id: string;
  name: string;
  description?: string;
  is_default: boolean;
  is_active: boolean;
  stages: PipelineStage[];
  created_at: string;
}

export interface Deal {
  id: string;
  tenant_id: string;
  name: string;
  value: number;
  currency: string;
  probability: number;
  expected_close_date?: string;
  actual_close_date?: string;
  pipeline_id: string;
  stage_id: string;
  company_id?: string;
  contact_id?: string;
  owner_id?: string;
  status: string;
  loss_reason?: string;
  custom_fields: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface KanbanColumn {
  stage_id: string;
  stage_name: string;
  probability: number;
  stage_type: string;
  deals: Deal[];
  total_value: number;
  deal_count: number;
}

export interface KanbanBoard {
  pipeline_id: string;
  pipeline_name: string;
  columns: KanbanColumn[];
}

export interface Activity {
  id: string;
  tenant_id: string;
  entity_type: string;
  entity_id: string;
  activity_type: string;
  title: string;
  description?: string;
  performed_at: string;
  duration_minutes?: number;
  outcome?: string;
  sentiment?: string;
  user_id?: string;
  metadata_json: Record<string, any>;
  created_at: string;
}

export interface Task {
  id: string;
  tenant_id: string;
  title: string;
  description?: string;
  priority: string;
  status: string;
  due_date?: string;
  completed_at?: string;
  entity_type?: string;
  entity_id?: string;
  assigned_to_id?: string;
  created_by_id?: string;
  is_recurring: boolean;
  recurrence_rule?: string;
  created_at: string;
  updated_at: string;
}

export interface CalendarEvent {
  id: string;
  tenant_id: string;
  title: string;
  description?: string;
  location?: string;
  meeting_url?: string;
  start_time: string;
  end_time: string;
  is_all_day: boolean;
  entity_type?: string;
  entity_id?: string;
  organizer_id: string;
  attendees: Array<{ email: string; name?: string; status: string; is_organizer: boolean }>;
  created_at: string;
}

export interface Product {
  id: string;
  tenant_id: string;
  name: string;
  sku: string;
  category_id?: string;
  description?: string;
  unit_price: number;
  currency: string;
  tax_rate_pct: number;
  is_active: boolean;
  is_service: boolean;
  inventory_stock: number;
  created_at: string;
}

export interface Proposal {
  id: string;
  tenant_id: string;
  proposal_number: string;
  title: string;
  status: string;
  deal_id?: string;
  company_id?: string;
  contact_id?: string;
  subtotal: number;
  discount_amount: number;
  tax_amount: number;
  total_amount: number;
  currency: string;
  valid_until?: string;
  created_at: string;
}

export interface Quote {
  id: string;
  tenant_id: string;
  quote_number: string;
  status: string;
  deal_id?: string;
  total_amount: number;
  currency: string;
  expiration_date?: string;
  created_at: string;
}

export interface Invoice {
  id: string;
  tenant_id: string;
  invoice_number: string;
  status: string;
  payment_status: string;
  issue_date: string;
  due_date: string;
  subtotal: number;
  tax_amount: number;
  total_amount: number;
  amount_paid: number;
  currency: string;
  created_at: string;
}

export interface Ticket {
  id: string;
  tenant_id: string;
  ticket_number: string;
  subject: string;
  description: string;
  priority: string;
  status: string;
  category: string;
  contact_id?: string;
  company_id?: string;
  assigned_to_id?: string;
  is_escalated: boolean;
  resolved_at?: string;
  resolution_notes?: string;
  created_at: string;
  updated_at: string;
}

export interface CustomerSuccessPlan {
  id: string;
  tenant_id: string;
  company_id: string;
  owner_id?: string;
  status: string;
  health_score: number;
  health_grade: string;
  target_renewal_date?: string;
  renewal_value?: number;
  churn_risk_reason?: string;
  goals: string[];
  milestones: Array<{ id: string; title: string; is_completed: boolean; due_date?: string }>;
  created_at: string;
}

export interface Campaign {
  id: string;
  tenant_id: string;
  name: string;
  type: string;
  status: string;
  segment_id?: string;
  template_id?: string;
  total_recipients: number;
  sent_count: number;
  open_count: number;
  click_count: number;
  conversion_count: number;
  revenue_attributed: number;
  created_at: string;
}

export interface AutomationWorkflow {
  id: string;
  tenant_id: string;
  name: string;
  description?: string;
  is_active: boolean;
  trigger_event: string;
  conditions: Array<{ id: string; field_path: string; operator: string; target_value: string }>;
  actions: Array<{ id: string; action_type: string; action_config: Record<string, any>; execution_order: number }>;
  created_at: string;
}

export interface DashboardMetrics {
  total_pipeline_value: { label: string; value: number; formatted_value: string; change_pct?: number; trend?: string };
  weighted_forecast: { label: string; value: number; formatted_value: string; change_pct?: number; trend?: string };
  win_rate: { label: string; value: number; formatted_value: string; change_pct?: number; trend?: string };
  active_deals_count: { label: string; value: number; formatted_value: string; change_pct?: number; trend?: string };
  lead_conversion_rate: { label: string; value: number; formatted_value: string; change_pct?: number; trend?: string };
  customer_avg_health: { label: string; value: number; formatted_value: string; change_pct?: number; trend?: string };
  sla_compliance_rate: { label: string; value: number; formatted_value: string; change_pct?: number; trend?: string };
  revenue_trend: Array<{ period: string; revenue: number; deals_count: number }>;
  conversion_funnel: Array<{ stage_name: string; count: number; value: number; conversion_rate_pct: number }>;
  rep_leaderboard: Array<{ user_id: string; user_name: string; deals_won_count: number; revenue_won: number; target: number; quota_attainment_pct: number }>;
}
""")

    # 2. frontend/src/services/api.ts
    write_file("frontend/src/services/api.ts", """import axios from "axios";

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
""")

    # 3. frontend/src/context/AuthContext.tsx
    write_file("frontend/src/context/AuthContext.tsx", """import React, { createContext, useContext, useState, useEffect } from "react";
import { User, Organization } from "../types";
import { api } from "../services/api";

interface AuthContextType {
  user: User | null;
  organization: Organization | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (tokens: { access_token: string; refresh_token: string; user: any; tenant_id?: string }) => void;
  logout: () => void;
  setOrganization: (org: Organization) => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [organization, setOrganization] = useState<Organization | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    const token = localStorage.getItem("clientflow_access_token");
    if (token) {
      api.getMe()
        .then((res) => {
          setUser(res.data);
          return api.getCurrentOrg();
        })
        .then((orgRes) => {
          setOrganization(orgRes.data);
        })
        .catch(() => {
          localStorage.removeItem("clientflow_access_token");
          localStorage.removeItem("clientflow_refresh_token");
          setUser(null);
        })
        .finally(() => setIsLoading(false));
    } else {
      setIsLoading(false);
    }
  }, []);

  const login = (tokens: { access_token: string; refresh_token: string; user: any; tenant_id?: string }) => {
    localStorage.setItem("clientflow_access_token", tokens.access_token);
    localStorage.setItem("clientflow_refresh_token", tokens.refresh_token);
    if (tokens.tenant_id) {
      localStorage.setItem("clientflow_tenant_id", tokens.tenant_id);
    }
    setUser(tokens.user);
    api.getCurrentOrg()
      .then((orgRes) => setOrganization(orgRes.data))
      .catch(() => {});
  };

  const logout = () => {
    localStorage.removeItem("clientflow_access_token");
    localStorage.removeItem("clientflow_refresh_token");
    localStorage.removeItem("clientflow_tenant_id");
    setUser(null);
    setOrganization(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        organization,
        isAuthenticated: !!user,
        isLoading,
        login,
        logout,
        setOrganization,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
""")

    print("Frontend Types, API Client & AuthContext generated.")

if __name__ == '__main__':
    run()
