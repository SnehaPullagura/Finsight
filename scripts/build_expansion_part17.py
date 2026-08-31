import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/customer_churn_predictor.py
    write_file("backend/app/enterprise/crm_analytics/customer_churn_predictor.py", """import math
from typing import Any, Dict, List, Optional

class LogisticChurnPredictor:
    # Feature weights: [logins_normalized, tickets_normalized, nps_normalized, overdue_invoices]
    WEIGHTS = [-2.5, 1.8, -1.2, 2.2]
    BIAS = 0.5

    @staticmethod
    def predict_churn_probability(
        logins_per_user_per_week: float, # 0 - 20
        open_tickets_count: int,          # 0 - 10
        nps_rating: int,                  # 0 - 10
        has_overdue_invoices: bool
    ) -> Dict[str, Any]:
        # Normalize features to 0-1
        f1 = min(1.0, logins_per_user_per_week / 10.0)
        f2 = min(1.0, open_tickets_count / 5.0)
        f3 = min(1.0, nps_rating / 10.0)
        f4 = 1.0 if has_overdue_invoices else 0.0

        z = (f1 * LogisticChurnPredictor.WEIGHTS[0]) + \
            (f2 * LogisticChurnPredictor.WEIGHTS[1]) + \
            (f3 * LogisticChurnPredictor.WEIGHTS[2]) + \
            (f4 * LogisticChurnPredictor.WEIGHTS[3]) + \
            LogisticChurnPredictor.BIAS

        prob = 1.0 / (1.0 + math.exp(-z))
        prob_pct = round(prob * 100.0, 1)

        tier = "Critical" if prob_pct >= 70 else "High" if prob_pct >= 40 else "Low"

        return {
            "churn_probability": round(prob, 4),
            "churn_probability_percentage": prob_pct,
            "risk_tier": tier,
            "is_action_required": prob_pct >= 40.0
        }
""")

    # 2. backend/app/enterprise/crm_analytics/sales_activity_productivity_index.py
    write_file("backend/app/enterprise/crm_analytics/sales_activity_productivity_index.py", """from typing import Any, Dict, List, Optional

class SalesActivityProductivityIndex:
    ACTIVITY_WEIGHTS = {
        "meeting": 10.0,
        "call": 3.0,
        "email": 1.0,
        "proposal_sent": 15.0,
        "contract_sent": 25.0
    }

    @staticmethod
    def calculate_rep_productivity(rep_activities: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_points = 0.0
        breakdown = {k: 0 for k in SalesActivityProductivityIndex.ACTIVITY_WEIGHTS.keys()}

        for act in rep_activities:
            atype = (act.get("activity_type") or "email").lower()
            weight = SalesActivityProductivityIndex.ACTIVITY_WEIGHTS.get(atype, 1.0)
            total_points += weight
            if atype in breakdown:
                breakdown[atype] += 1

        # Benchmark: 100 points per week is target productivity
        target = 100.0
        productivity_index = round((total_points / target) * 100.0, 1)

        return {
            "total_productivity_points": round(total_points, 1),
            "target_productivity_points": target,
            "productivity_index_pct": productivity_index,
            "activity_counts": breakdown,
            "rating": "High Performer" if productivity_index >= 120 else "On Track" if productivity_index >= 90 else "Underperforming"
        }
""")

    # 3. backend/app/enterprise/data_pipeline/bulk_upsert_coordinator.py
    write_file("backend/app/enterprise/data_pipeline/bulk_upsert_coordinator.py", """from typing import Any, Dict, List, Tuple

class BulkUpsertCoordinator:
    @staticmethod
    def partition_inserts_and_updates(
        incoming_batch: List[Dict[str, Any]],
        existing_lookup: Dict[str, str], # email/key -> existing_id
        match_key: str = "email"
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        inserts = []
        updates = []

        for row in incoming_batch:
            key_val = (row.get(match_key) or "").lower().strip()
            if key_val in existing_lookup:
                row_copy = dict(row)
                row_copy["id"] = existing_lookup[key_val]
                updates.append(row_copy)
            else:
                inserts.append(row)

        return inserts, updates
""")

    # 4. frontend/src/enterprise/EnterprisePipelineVelocityHeatmap.tsx
    write_file("frontend/src/enterprise/EnterprisePipelineVelocityHeatmap.tsx", """import React, { useState } from "react";
import { Zap, Clock, TrendingUp, AlertTriangle, CheckCircle2 } from "lucide-react";

export const EnterprisePipelineVelocityHeatmap: React.FC = () => {
  const stages = [
    { name: "Discovery", avgDays: 4.2, benchmark: 5.0, status: "healthy" },
    { name: "Scoping & Architecture", avgDays: 8.5, benchmark: 7.0, status: "warning" },
    { name: "Proposal & Pricing", avgDays: 5.1, benchmark: 6.0, status: "healthy" },
    { name: "Executive Negotiation", avgDays: 14.8, benchmark: 10.0, status: "critical" },
    { name: "Legal & Procurement", avgDays: 12.0, benchmark: 14.0, status: "healthy" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Zap className="w-5 h-5 text-emerald-400" />
            Deal Stage Velocity & Stagnation Heatmap
          </h3>
          <p className="text-xs text-slate-400">Identify pipeline friction points and stage stagnation bottlenecks across sales cycles</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
        {stages.map((stg, idx) => (
          <div key={idx} className={`p-4 rounded-xl border ${
            stg.status === "critical" ? "bg-red-950/30 border-red-800" :
            stg.status === "warning" ? "bg-amber-950/30 border-amber-800" : "bg-slate-950 border-slate-800"
          }`}>
            <span className="text-[11px] text-slate-400 font-semibold block">{stg.name}</span>
            <div className="text-xl font-bold text-white mt-1">{stg.avgDays} Days</div>
            <div className="text-[10px] text-slate-500 mt-2 flex justify-between">
              <span>Goal: {stg.benchmark}d</span>
              <span className={stg.status === "critical" ? "text-red-400 font-bold" : stg.status === "warning" ? "text-amber-400" : "text-emerald-400"}>
                {stg.status.toUpperCase()}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    print("Created churn predictor, productivity index, bulk upsert, and velocity heatmap.")

if __name__ == '__main__':
    run()
