export interface User {
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
