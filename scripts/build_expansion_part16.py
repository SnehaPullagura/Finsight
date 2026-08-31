import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/revenue_cohort_analyzer.py
    write_file("backend/app/enterprise/crm_analytics/revenue_cohort_analyzer.py", """from datetime import date
from typing import Any, Dict, List, Optional
from collections import defaultdict

class RevenueCohortAnalyzer:
    @staticmethod
    def calculate_cohort_retention_matrix(
        customer_signups: List[Dict[str, Any]],
        monthly_billings: List[Dict[str, Any]],
        periods_months: int = 12
    ) -> List[Dict[str, Any]]:
        # Cohort calculation: Track initial cohort size and percentage retention over time
        cohorts = defaultdict(lambda: {"initial_count": 0, "initial_mrr": 0.0, "retention_by_period": [0.0] * periods_months})

        for cust in customer_signups:
            cohort_month = cust.get("signup_month", "2026-01")
            cohorts[cohort_month]["initial_count"] += 1
            cohorts[cohort_month]["initial_mrr"] += float(cust.get("initial_mrr", 0.0))

        for bill in monthly_billings:
            cohort_month = bill.get("cohort_month")
            period_idx = int(bill.get("period_index", 0))
            if cohort_month in cohorts and 0 <= period_idx < periods_months:
                cohorts[cohort_month]["retention_by_period"][period_idx] += float(bill.get("mrr_amount", 0.0))

        result_matrix = []
        for cmonth, data in sorted(cohorts.items()):
            init_mrr = max(1.0, data["initial_mrr"])
            pct_retention = [round((p / init_mrr) * 100.0, 1) for p in data["retention_by_period"]]
            result_matrix.append({
                "cohort_month": cmonth,
                "customer_count": data["initial_count"],
                "initial_mrr": round(data["initial_mrr"], 2),
                "retention_percentages": pct_retention
            })

        return result_matrix
""")

    # 2. backend/app/enterprise/crm_analytics/lead_conversion_velocity_model.py
    write_file("backend/app/enterprise/crm_analytics/lead_conversion_velocity_model.py", """from datetime import date
from typing import Any, Dict, List, Optional

class LeadConversionVelocityModel:
    @staticmethod
    def calculate_sales_cycle_velocity(
        qualified_leads: int,
        win_rate_pct: float,
        average_deal_size: float,
        sales_cycle_days: float
    ) -> Dict[str, Any]:
        win_rate_decimal = win_rate_pct / 100.0
        cycle_days = max(1.0, sales_cycle_days)
        
        # Pipeline Velocity Formula: V = (Leads * WinRate * DealSize) / CycleLengthDays
        daily_velocity = (qualified_leads * win_rate_decimal * average_deal_size) / cycle_days
        monthly_velocity = daily_velocity * 30.0
        annual_velocity = daily_velocity * 365.0

        return {
            "qualified_leads_count": qualified_leads,
            "win_rate_percentage": win_rate_pct,
            "average_deal_size": average_deal_size,
            "sales_cycle_length_days": sales_cycle_days,
            "daily_revenue_velocity": round(daily_velocity, 2),
            "monthly_projected_velocity": round(monthly_velocity, 2),
            "annual_projected_velocity": round(annual_velocity, 2)
        }
""")

    # 3. backend/app/enterprise/data_pipeline/cdc_stream_handler.py
    write_file("backend/app/enterprise/data_pipeline/cdc_stream_handler.py", """import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class ChangeDataCaptureStreamHandler:
    def __init__(self):
        self.cdc_log = []

    def capture_change(
        self,
        table_name: str,
        operation: str, # INSERT, UPDATE, DELETE
        primary_key: str,
        before_state: Optional[Dict[str, Any]],
        after_state: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        cdc_entry = {
            "cdc_id": f"cdc_{int(datetime.now(timezone.utc).timestamp() * 1000)}",
            "table_name": table_name,
            "operation": operation.upper(),
            "primary_key": primary_key,
            "before": before_state,
            "after": after_state,
            "captured_at": datetime.now(timezone.utc).isoformat()
        }
        self.cdc_log.append(cdc_entry)
        return cdc_entry
""")

    # 4. frontend/src/enterprise/EnterpriseCohortRetentionStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseCohortRetentionStudio.tsx", """import React, { useState } from "react";
import { Users, TrendingUp, Filter, CheckCircle2, DollarSign } from "lucide-react";

export const EnterpriseCohortRetentionStudio: React.FC = () => {
  const cohorts = [
    { month: "Jan 2026", size: 45, m0: "100%", m1: "98%", m2: "96%", m3: "95%", m4: "94%", m5: "94%" },
    { month: "Feb 2026", size: 52, m0: "100%", m1: "97%", m2: "95%", m3: "95%", m4: "93%", m5: "-" },
    { month: "Mar 2026", size: 60, m0: "100%", m1: "99%", m2: "97%", m3: "96%", m4: "-", m5: "-" },
    { month: "Apr 2026", size: 75, m0: "100%", m1: "98%", m2: "96%", m3: "-", m4: "-", m5: "-" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Users className="w-5 h-5 text-emerald-400" />
            Customer & Revenue Cohort Retention Matrix
          </h3>
          <p className="text-xs text-slate-400">Monthly Net Revenue Retention (NRR) heatmap across customer acquisition cohorts</p>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-xs text-left">
          <thead className="bg-slate-950 text-slate-400 font-semibold border-b border-slate-800">
            <tr>
              <th className="p-3">Cohort</th>
              <th className="p-3 text-right">Accounts</th>
              <th className="p-3 text-center">Month 0</th>
              <th className="p-3 text-center">Month 1</th>
              <th className="p-3 text-center">Month 2</th>
              <th className="p-3 text-center">Month 3</th>
              <th className="p-3 text-center">Month 4</th>
              <th className="p-3 text-center">Month 5</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-white">
            {cohorts.map((c, idx) => (
              <tr key={idx} className="hover:bg-slate-800/30">
                <td className="p-3 font-semibold">{c.month}</td>
                <td className="p-3 text-right text-slate-400">{c.size}</td>
                <td className="p-3 text-center font-bold text-emerald-400">{c.m0}</td>
                <td className="p-3 text-center text-emerald-400">{c.m1}</td>
                <td className="p-3 text-center text-emerald-400">{c.m2}</td>
                <td className="p-3 text-center text-emerald-400">{c.m3}</td>
                <td className="p-3 text-center text-emerald-400">{c.m4}</td>
                <td className="p-3 text-center text-emerald-400">{c.m5}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
""")

    print("Created revenue cohort analyzer, velocity model, CDC stream, and Cohort UI.")

if __name__ == '__main__':
    run()
