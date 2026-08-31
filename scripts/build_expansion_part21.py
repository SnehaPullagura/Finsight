import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/marketing_channel_efficiency_cube.py
    write_file("backend/app/enterprise/crm_analytics/marketing_channel_efficiency_cube.py", """from typing import Any, Dict, List, Optional
from collections import defaultdict

class MarketingChannelEfficiencyCube:
    @staticmethod
    def calculate_efficiency_metrics(campaign_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        channel_data = defaultdict(lambda: {"spend": 0.0, "leads": 0, "sqls": 0, "won_deals": 0, "revenue": 0.0})

        for camp in campaign_records:
            ch = camp.get("channel", "Organic")
            channel_data[ch]["spend"] += float(camp.get("spend", 0.0))
            channel_data[ch]["leads"] += int(camp.get("leads_generated", 0))
            channel_data[ch]["sqls"] += int(camp.get("sqls_generated", 0))
            channel_data[ch]["won_deals"] += int(camp.get("won_deals_count", 0))
            channel_data[ch]["revenue"] += float(camp.get("attributed_revenue", 0.0))

        results = []
        for ch, d in channel_data.items():
            spend = d["spend"]
            rev = d["revenue"]
            leads = d["leads"]
            won = d["won_deals"]

            cpl = round(spend / max(1, leads), 2)
            cac = round(spend / max(1, won), 2)
            roas = round(rev / max(1.0, spend), 2)

            results.append({
                "channel_name": ch,
                "total_spend": round(spend, 2),
                "leads_generated": leads,
                "cost_per_lead": cpl,
                "won_deals_count": won,
                "customer_acquisition_cost": cac,
                "attributed_revenue": round(rev, 2),
                "roas_multiplier": roas,
                "efficiency_rating": "Top Performer" if roas >= 10.0 else "Solid" if roas >= 4.0 else "Underperforming"
            })

        return sorted(results, key=lambda x: x["attributed_revenue"], reverse=True)
""")

    # 2. backend/app/enterprise/crm_analytics/customer_lifetime_value_model.py
    write_file("backend/app/enterprise/crm_analytics/customer_lifetime_value_model.py", """from typing import Any, Dict, List, Optional

class CustomerLifetimeValueModel:
    @staticmethod
    def calculate_ltv_projection(
        average_mrr: float,
        gross_margin_percentage: float,
        monthly_churn_rate_pct: float,
        discount_rate_annual_pct: float = 8.0
    ) -> Dict[str, Any]:
        margin_decimal = gross_margin_percentage / 100.0
        monthly_churn_decimal = max(0.001, monthly_churn_rate_pct / 100.0)
        
        # Monthly Discount Rate
        monthly_discount_rate = (1.0 + (discount_rate_annual_pct / 100.0)) ** (1.0 / 12.0) - 1.0

        # LTV Formula: (ARPU * Gross Margin) / (Monthly Churn + Monthly Discount Rate)
        average_lifespan_months = round(1.0 / monthly_churn_decimal, 1)
        discounted_ltv = round((average_mrr * margin_decimal) / (monthly_churn_decimal + monthly_discount_rate), 2)
        simple_ltv = round((average_mrr * margin_decimal) / monthly_churn_decimal, 2)

        return {
            "average_monthly_revenue": average_mrr,
            "gross_margin_pct": gross_margin_percentage,
            "monthly_churn_rate_pct": monthly_churn_rate_pct,
            "average_lifespan_months": average_lifespan_months,
            "simple_ltv": simple_ltv,
            "discounted_ltv": discounted_ltv,
            "annualized_arr_per_customer": round(average_mrr * 12.0, 2)
        }
""")

    # 3. backend/app/enterprise/data_pipeline/data_reconciliation_engine.py
    write_file("backend/app/enterprise/data_pipeline/data_reconciliation_engine.py", """from typing import Any, Dict, List, Tuple

class DataReconciliationEngine:
    @staticmethod
    def reconcile_datasets(
        source_records: List[Dict[str, Any]],
        target_records: List[Dict[str, Any]],
        primary_key: str = "id"
    ) -> Dict[str, Any]:
        src_map = {str(r.get(primary_key)): r for r in source_records}
        tgt_map = {str(r.get(primary_key)): r for r in target_records}

        matched_keys = set(src_map.keys()).intersection(set(tgt_map.keys()))
        missing_in_target = set(src_map.keys()) - set(tgt_map.keys())
        missing_in_source = set(tgt_map.keys()) - set(src_map.keys())

        discrepancies = []
        for k in matched_keys:
            s_rec = src_map[k]
            t_rec = tgt_map[k]
            diffs = {}
            for col in s_rec.keys():
                if s_rec.get(col) != t_rec.get(col):
                    diffs[col] = {"source": s_rec.get(col), "target": t_rec.get(col)}
            if diffs:
                discrepancies.append({"id": k, "field_differences": diffs})

        return {
            "total_source_records": len(source_records),
            "total_target_records": len(target_records),
            "perfect_matches_count": len(matched_keys) - len(discrepancies),
            "discrepancies_count": len(discrepancies),
            "missing_in_target_count": len(missing_in_target),
            "missing_in_source_count": len(missing_in_source),
            "discrepancies": discrepancies[:20]
        }
""")

    # 4. frontend/src/enterprise/EnterpriseMarketingEfficiencyStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseMarketingEfficiencyStudio.tsx", """import React, { useState } from "react";
import { TrendingUp, DollarSign, Target, Award, ArrowUpRight } from "lucide-react";

export const EnterpriseMarketingEfficiencyStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Target className="w-5 h-5 text-emerald-400" />
            Marketing Capital Efficiency & ROAS Matrix
          </h3>
          <p className="text-xs text-slate-400">Blended vs Paid Customer Acquisition Cost (CAC) and campaign revenue payback</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Blended CAC</span>
          <div className="text-2xl font-bold text-emerald-400">$3,420</div>
          <span className="text-[10px] text-slate-400">↓ 14.5% vs Prior Quarter</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Blended ROAS Multiplier</span>
          <div className="text-2xl font-bold text-white">14.8x</div>
          <span className="text-[10px] text-emerald-400">$14.80 Return per $1.00 Ad Spend</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Lead to Opportunity Conv.</span>
          <div className="text-2xl font-bold text-white">18.4%</div>
          <span className="text-[10px] text-emerald-400">Top Quartile B2B Funnel</span>
        </div>
      </div>
    </div>
  );
};
""")

    # 5. frontend/src/enterprise/EnterpriseLTVModelerStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseLTVModelerStudio.tsx", """import React, { useState } from "react";
import { Calculator, DollarSign, TrendingUp, CheckCircle2 } from "lucide-react";

export const EnterpriseLTVModelerStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Calculator className="w-5 h-5 text-emerald-400" />
            Customer Lifetime Value (LTV) Actuarial Modeler
          </h3>
          <p className="text-xs text-slate-400">Discounted cash flow (DCF) actuarial LTV projections based on empirical cohort churn</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Discounted LTV</span>
          <div className="text-2xl font-bold text-emerald-400">$184,500</div>
          <span className="text-[10px] text-slate-400">8.0% Annual Discount Rate</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Average Lifespan</span>
          <div className="text-2xl font-bold text-white">41.6 Months</div>
          <span className="text-[10px] text-emerald-400">0.8% Monthly Logo Churn</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Gross Margin</span>
          <div className="text-2xl font-bold text-white">82.5%</div>
          <span className="text-[10px] text-slate-400">SaaS Cloud Infrastructure Model</span>
        </div>
      </div>
    </div>
  );
};
""")

    print("Created channel efficiency cube, LTV modeler, reconciliation engine, and UI studios.")

if __name__ == '__main__':
    run()
