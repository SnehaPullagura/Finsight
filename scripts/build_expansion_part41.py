import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/executive_sales_rep_activity_roi.py
    write_file("backend/app/enterprise/crm_analytics/executive_sales_rep_activity_roi.py", """from typing import Any, Dict, List, Optional

class RepActivityROIAnalyzer:
    @staticmethod
    def calculate_activity_effectiveness(reps_activities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for r in reps_activities:
            name = r.get("rep_name")
            calls = int(r.get("calls_completed", 0))
            demos = int(r.get("demos_conducted", 0))
            emails = int(r.get("emails_sent", 0))
            won_rev = float(r.get("closed_won_revenue", 0.0))

            total_activities = calls + demos + emails
            rev_per_activity = round(won_rev / max(1, total_activities), 2)
            demo_to_won_rate = round((int(r.get("deals_won_count", 0)) / max(1, demos)) * 100.0, 1)

            results.append({
                "rep_name": name,
                "total_sales_activities": total_activities,
                "closed_won_revenue": won_rev,
                "revenue_per_activity": rev_per_activity,
                "demo_to_won_conversion_pct": demo_to_won_rate,
                "efficiency_tier": "High Leverage" if rev_per_activity >= 500.0 else "Solid Contributor" if rev_per_activity >= 250.0 else "High Volume / Low Conversion"
            })

        return sorted(results, key=lambda x: x["revenue_per_activity"], reverse=True)
""")

    # 2. backend/app/enterprise/crm_analytics/marketing_creative_performance_index.py
    write_file("backend/app/enterprise/crm_analytics/marketing_creative_performance_index.py", """from typing import Any, Dict, List, Optional

class MarketingCreativePerformanceIndex:
    @staticmethod
    def calculate_creative_roi(creatives: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for c in creatives:
            spend = float(c.get("spend", 1000.0))
            rev = float(c.get("attributed_revenue", 0.0))
            clicks = int(c.get("clicks", 100))
            impressions = int(c.get("impressions", 10000))

            roas = round(rev / max(1.0, spend), 2)
            ctr = round((clicks / max(1, impressions)) * 100.0, 2)
            cpc = round(spend / max(1, clicks), 2)

            results.append({
                "creative_name": c.get("name"),
                "ad_format": c.get("format", "Video"),
                "roas_multiplier": roas,
                "click_through_rate_pct": ctr,
                "cost_per_click": cpc,
                "performance_tier": "Top Performer (ROAS > 8x)" if roas >= 8.0 else "Solid (4x - 8x)" if roas >= 4.0 else "Underperforming (< 4x)"
            })

        return sorted(results, key=lambda x: x["roas_multiplier"], reverse=True)
""")

    # 3. frontend/src/enterprise/EnterpriseActivityROIScorecard.tsx
    write_file("frontend/src/enterprise/EnterpriseActivityROIScorecard.tsx", """import React, { useState } from "react";
import { Activity, DollarSign, Award, TrendingUp, CheckCircle2 } from "lucide-react";

export const EnterpriseActivityROIScorecard: React.FC = () => {
  const reps = [
    { name: "Alex Vance", activities: 240, wonRev: "$280,000", revPerAct: "$1,166", demoConv: "48.5%", rating: "High Leverage" },
    { name: "Sarah Connor", activities: 380, wonRev: "$310,000", revPerAct: "$815", demoConv: "42.0%", rating: "High Leverage" },
    { name: "John Wick", activities: 410, wonRev: "$140,000", revPerAct: "$341", demoConv: "24.0%", rating: "Solid Contributor" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Activity className="w-5 h-5 text-emerald-400" />
            Sales Rep Activity ROI & Conversion Efficiency
          </h3>
          <p className="text-xs text-slate-400">Revenue generated per sales touchpoint and demo-to-close win rates</p>
        </div>
      </div>

      <div className="space-y-3">
        {reps.map((r, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{r.name}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">
                {r.activities} activities • {r.wonRev} Won • Demo Close: {r.demoConv}
              </div>
            </div>
            <div className="text-right">
              <span className="text-sm font-bold text-emerald-400">{r.revPerAct} / Activity</span>
              <span className="text-[10px] text-slate-500 block">{r.rating}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    # 4. frontend/src/enterprise/EnterpriseCreativePerformanceMatrix.tsx
    write_file("frontend/src/enterprise/EnterpriseCreativePerformanceMatrix.tsx", """import React, { useState } from "react";
import { Target, TrendingUp, DollarSign, Award, CheckCircle2 } from "lucide-react";

export const EnterpriseCreativePerformanceMatrix: React.FC = () => {
  const creatives = [
    { name: "Executive CPQ Interactive Product Tour", format: "Interactive Video", roas: "12.4x", ctr: "3.8%", cpc: "$4.12", tier: "Top Performer" },
    { name: "Multi-Tenant Enterprise Security Benchmark", format: "PDF Whitepaper", roas: "8.6x", ctr: "2.9%", cpc: "$5.80", tier: "Top Performer" },
    { name: "Salesforce Migration TCO Calculator", format: "Web Calculator", roas: "5.2x", ctr: "2.1%", cpc: "$7.20", tier: "Solid" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Target className="w-5 h-5 text-emerald-400" />
            Marketing Creative Performance & Return on Ad Spend (ROAS)
          </h3>
          <p className="text-xs text-slate-400">Attributed pipeline revenue multipliers by ad creative and interactive asset</p>
        </div>
      </div>

      <div className="space-y-3">
        {creatives.map((c, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{c.name}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Format: {c.format} • CTR: {c.ctr} • CPC: {c.cpc}</div>
            </div>
            <div className="text-right">
              <span className="text-sm font-bold text-emerald-400">{c.roas} ROAS</span>
              <span className="text-[10px] text-slate-500 block">{c.tier}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    print("Created activity ROI analyzer, creative performance index, and UI studios.")

if __name__ == '__main__':
    run()
