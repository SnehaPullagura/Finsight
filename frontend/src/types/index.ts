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
