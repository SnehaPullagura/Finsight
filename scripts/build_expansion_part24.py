import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/marketing_mql_to_sql_funnel_model.py
    write_file("backend/app/enterprise/crm_analytics/marketing_mql_to_sql_funnel_model.py", """from typing import Any, Dict, List, Optional

class FunnelConversionModel:
    @staticmethod
    def calculate_full_funnel_metrics(
        visitor_count: int,
        lead_count: int,
        mql_count: int,
        sql_count: int,
        opportunity_count: int,
        won_deal_count: int
    ) -> Dict[str, Any]:
        v_to_lead = round((lead_count / max(1, visitor_count)) * 100.0, 2)
        lead_to_mql = round((mql_count / max(1, lead_count)) * 100.0, 2)
        mql_to_sql = round((sql_count / max(1, mql_count)) * 100.0, 2)
        sql_to_opp = round((opportunity_count / max(1, sql_count)) * 100.0, 2)
        opp_to_won = round((won_deal_count / max(1, opportunity_count)) * 100.0, 2)
        overall_conversion = round((won_deal_count / max(1, visitor_count)) * 100.0, 3)

        return {
            "funnel_stages": [
                {"stage": "Website Visitors", "count": visitor_count, "conversion_to_next": v_to_lead},
                {"stage": "Inbound Leads", "count": lead_count, "conversion_to_next": lead_to_mql},
                {"stage": "Marketing Qualified (MQL)", "count": mql_count, "conversion_to_next": mql_to_sql},
                {"stage": "Sales Qualified (SQL)", "count": sql_count, "conversion_to_next": sql_to_opp},
                {"stage": "Sales Opportunities", "count": opportunity_count, "conversion_to_next": opp_to_won},
                {"stage": "Closed Won Deals", "count": won_deal_count, "conversion_to_next": 100.0}
            ],
            "overall_visitor_to_customer_pct": overall_conversion,
            "funnel_health": "High Efficiency" if mql_to_sql >= 40.0 and opp_to_won >= 25.0 else "Needs SDR Optimization"
        }
""")

    # 2. backend/app/enterprise/crm_analytics/customer_expansion_opportunity_finder.py
    write_file("backend/app/enterprise/crm_analytics/customer_expansion_opportunity_finder.py", """from typing import Any, Dict, List, Optional

class CustomerExpansionOpportunityFinder:
    @staticmethod
    def identify_upsell_candidates(accounts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        expansion_candidates = []

        for acc in accounts:
            seats_used = int(acc.get("seats_used", 0))
            seats_purchased = int(acc.get("seats_purchased", 1))
            health_score = int(acc.get("health_score", 50))
            arr = float(acc.get("current_arr", 0.0))

            utilization_pct = round((seats_used / max(1, seats_purchased)) * 100.0, 1)

            # High utilization (>= 90%) + High health (>= 80) -> Upsell Candidate
            if utilization_pct >= 90.0 and health_score >= 80:
                recommended_add_seats = max(5, int(seats_purchased * 0.25))
                projected_expansion_arr = round(arr * 0.25, 2)

                expansion_candidates.append({
                    "account_id": acc.get("id"),
                    "account_name": acc.get("name"),
                    "utilization_percentage": utilization_pct,
                    "health_score": health_score,
                    "current_arr": arr,
                    "recommended_additional_seats": recommended_add_seats,
                    "projected_expansion_arr": projected_expansion_arr,
                    "signal": "High license utilization approaching ceiling"
                })

        return sorted(expansion_candidates, key=lambda x: x["projected_expansion_arr"], reverse=True)
""")

    # 3. frontend/src/enterprise/EnterpriseFunnelConversionSankey.tsx
    write_file("frontend/src/enterprise/EnterpriseFunnelConversionSankey.tsx", """import React, { useState } from "react";
import { Filter, TrendingUp, CheckCircle2, ArrowRight } from "lucide-react";

export const EnterpriseFunnelConversionSankey: React.FC = () => {
  const steps = [
    { name: "Website Visitors", count: "125,000", conv: "2.4% to Lead" },
    { name: "Inbound Leads", count: "3,000", conv: "45.0% to MQL" },
    { name: "Marketing Qualified (MQL)", count: "1,350", conv: "52.0% to SQL" },
    { name: "Sales Qualified (SQL)", count: "702", conv: "38.0% to Opp" },
    { name: "Opportunities", count: "266", conv: "32.0% to Won" },
    { name: "Closed Won Customers", count: "85", conv: "100%" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Filter className="w-5 h-5 text-emerald-400" />
            Full-Funnel Sales & Marketing Velocity Pipeline
          </h3>
          <p className="text-xs text-slate-400">End-to-end stage conversion rates from visitor acquisition to closed-won revenue</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-6 gap-2">
        {steps.map((st, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-3 rounded-xl space-y-1">
            <span className="text-[10px] text-slate-400 font-semibold uppercase truncate block">{st.name}</span>
            <div className="text-lg font-bold text-white">{st.count}</div>
            <span className="text-[10px] text-emerald-400 font-medium block">{st.conv}</span>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    # 4. frontend/src/enterprise/EnterpriseExpansionOpportunityMatrix.tsx
    write_file("frontend/src/enterprise/EnterpriseExpansionOpportunityMatrix.tsx", """import React, { useState } from "react";
import { TrendingUp, Users, DollarSign, CheckCircle2, ChevronRight } from "lucide-react";

export const EnterpriseExpansionOpportunityMatrix: React.FC = () => {
  const candidates = [
    { name: "Wayne Enterprises", utilization: "98%", health: "95 / 100", currentArr: "$250,000", expansionArr: "+$62,500" },
    { name: "Stark Industries", utilization: "94%", health: "92 / 100", currentArr: "$180,000", expansionArr: "+$45,000" },
    { name: "Cyberdyne Systems", utilization: "91%", health: "88 / 100", currentArr: "$95,000", expansionArr: "+$23,750" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-emerald-400" />
            Customer Expansion & Upsell Opportunity Radar
          </h3>
          <p className="text-xs text-slate-400">High-health accounts approaching seat capacity thresholds</p>
        </div>
      </div>

      <div className="space-y-3">
        {candidates.map((c, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{c.name}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">
                License Utilization: {c.utilization} • Health Score: {c.health} • Base ARR: {c.currentArr}
              </div>
            </div>
            <div className="text-right">
              <span className="text-[10px] text-slate-500 uppercase font-semibold">Expansion Potential</span>
              <div className="text-sm font-bold text-emerald-400">{c.expansionArr}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    print("Created funnel model, expansion finder, and UI modules.")

if __name__ == '__main__':
    run()
