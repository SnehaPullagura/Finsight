import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/domain_services/billing_proration_calculator.py
    write_file("backend/app/domain_services/billing_proration_calculator.py", """from datetime import date, timedelta
from typing import Any, Dict, List, Optional

class BillingProrationCalculator:
    @staticmethod
    def calculate_mid_cycle_upgrade(
        old_plan_mrr: float,
        new_plan_mrr: float,
        billing_cycle_start: date,
        billing_cycle_end: date,
        effective_date: date
    ) -> Dict[str, float]:
        total_cycle_days = max(1, (billing_cycle_end - billing_cycle_start).days)
        days_used = max(0, (effective_date - billing_cycle_start).days)
        days_remaining = max(0, (billing_cycle_end - effective_date).days)

        unused_fraction = days_remaining / float(total_cycle_days)

        unused_old_plan_credit = round(old_plan_mrr * unused_fraction, 2)
        prorated_new_plan_charge = round(new_plan_mrr * unused_fraction, 2)
        immediate_charge = max(0.0, round(prorated_new_plan_charge - unused_old_plan_credit, 2))

        return {
            "cycle_days_total": total_cycle_days,
            "days_used": days_used,
            "days_remaining": days_remaining,
            "unused_credit_amount": unused_old_plan_credit,
            "prorated_charge_amount": prorated_new_plan_charge,
            "immediate_amount_due": immediate_charge,
            "next_cycle_mrr": round(new_plan_mrr, 2)
        }
""")

    # 2. backend/app/domain_services/support_ticket_router.py
    write_file("backend/app/domain_services/support_ticket_router.py", """from typing import Any, Dict, List, Optional

class SupportTicketRouter:
    CATEGORY_SKILL_MAP = {
        "billing": ["Finance", "Billing Specialist"],
        "technical": ["Tier 2 Support", "DevOps", "Integration Engineer"],
        "security": ["Security Team", "Compliance Officer"],
        "general": ["Tier 1 Support", "Customer Success"]
    }

    @staticmethod
    def calculate_priority_score(
        category: str,
        customer_tier: str, # enterprise, growth, starter
        sentiment_score: float, # -1.0 to 1.0
        is_sla_breached: bool = False
    ) -> str:
        score = 0
        
        # Customer tier weighting
        if customer_tier.lower() == "enterprise":
            score += 40
        elif customer_tier.lower() == "growth":
            score += 20

        # Category weighting
        if category.lower() == "security":
            score += 40
        elif category.lower() == "billing":
            score += 25
        elif category.lower() == "technical":
            score += 20

        # Sentiment factor
        if sentiment_score < -0.5:
            score += 20

        if is_sla_breached:
            score += 30

        if score >= 70:
            return "critical"
        elif score >= 45:
            return "high"
        elif score >= 25:
            return "medium"
        return "low"
""")

    # 3. backend/app/domain_services/custom_field_validator.py
    write_file("backend/app/domain_services/custom_field_validator.py", """import re
from typing import Any, Dict, List, Tuple

class CustomFieldValidator:
    @staticmethod
    def validate_field_value(field_def: Dict[str, Any], value: Any) -> Tuple[bool, Optional[str]]:
        field_name = field_def.get("name", "Field")
        field_type = field_def.get("type", "text")
        is_required = field_def.get("required", False)

        if is_required and (value is None or value == ""):
            return False, f"{field_name} is required."

        if value is None or value == "":
            return True, None

        if field_type == "number":
            try:
                float(value)
            except ValueError:
                return False, f"{field_name} must be a valid numeric value."

        elif field_type == "email":
            if not re.match(r"^[^@]+@[^@]+\.[^@]+$", str(value)):
                return False, f"{field_name} must be a valid email address."

        elif field_type == "select":
            allowed = field_def.get("options", [])
            if allowed and str(value) not in allowed:
                return False, f"{field_name} must be one of: {', '.join(allowed)}."

        return True, None
""")

    # 4. frontend/src/components/enterprise/DataAnalyticsStudio.tsx
    write_file("frontend/src/components/enterprise/DataAnalyticsStudio.tsx", """import React, { useState } from "react";
import { TrendingUp, Activity, PieChart, Users, DollarSign, Layers } from "lucide-react";
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

const TELEMETRY_DATA = [
  { day: "Mon", active_users: 120, api_calls: 45000, pipeline_added: 80000 },
  { day: "Tue", active_users: 145, api_calls: 52000, pipeline_added: 120000 },
  { day: "Wed", active_users: 160, api_calls: 61000, pipeline_added: 95000 },
  { day: "Thu", active_users: 180, api_calls: 78000, pipeline_added: 210000 },
  { day: "Fri", active_users: 195, api_calls: 84000, pipeline_added: 340000 },
  { day: "Sat", active_users: 85, api_calls: 31000, pipeline_added: 45000 },
  { day: "Sun", active_users: 70, api_calls: 28000, pipeline_added: 20000 }
];

export const DataAnalyticsStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Activity className="w-5 h-5 text-emerald-400" />
            Platform Telemetry & Operational Analytics
          </h3>
          <p className="text-xs text-slate-400">High-velocity telemetry across pipeline creation, API usage, and user activity</p>
        </div>
      </div>

      <div className="h-64 bg-slate-950 p-4 rounded-xl border border-slate-800">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={TELEMETRY_DATA}>
            <defs>
              <linearGradient id="colorPipeline" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#10b981" stopOpacity={0.4}/>
                <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis dataKey="day" stroke="#64748b" fontSize={11} />
            <YAxis stroke="#64748b" fontSize={11} tickFormatter={val => `$${val/1000}k`} />
            <Tooltip
              contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", borderRadius: "8px", fontSize: "11px" }}
              itemStyle={{ color: "#10b981" }}
            />
            <Area type="monotone" dataKey="pipeline_added" stroke="#10b981" fillOpacity={1} fill="url(#colorPipeline)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
""")

    print("Created proration calculator, ticket router, field validator, and DataAnalyticsStudio.")

if __name__ == '__main__':
    run()
