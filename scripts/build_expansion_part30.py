import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/marketing_channel_synergy_modeler.py
    write_file("backend/app/enterprise/crm_analytics/marketing_channel_synergy_modeler.py", """from typing import Any, Dict, List, Optional
from collections import defaultdict

class MarketingChannelSynergyModeler:
    @staticmethod
    def calculate_multi_touch_synergy_lift(journey_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        single_touch_conversions = 0
        multi_touch_conversions = 0
        single_touch_total = 0
        multi_touch_total = 0

        for j in journey_records:
            channels = j.get("touchpoint_channels", [])
            converted = bool(j.get("is_converted", False))

            if len(channels) <= 1:
                single_touch_total += 1
                if converted:
                    single_touch_conversions += 1
            else:
                multi_touch_total += 1
                if converted:
                    multi_touch_conversions += 1

        single_rate = round((single_touch_conversions / max(1, single_touch_total)) * 100.0, 1)
        multi_rate = round((multi_touch_conversions / max(1, multi_touch_total)) * 100.0, 1)
        synergy_lift = round(multi_rate - single_rate, 1)

        return {
            "single_channel_conversion_pct": single_rate,
            "multi_channel_conversion_pct": multi_rate,
            "synergy_lift_percentage": synergy_lift,
            "is_omnichannel_strategy_validated": synergy_lift > 5.0
        }
""")

    # 2. backend/app/enterprise/crm_analytics/sales_rep_quota_attainment_pacing.py
    write_file("backend/app/enterprise/crm_analytics/sales_rep_quota_attainment_pacing.py", """from datetime import date
from typing import Any, Dict, List, Optional

class QuotaAttainmentPacingModeler:
    @staticmethod
    def calculate_pacing_trajectory(
        quarter_quota: float,
        actual_closed_revenue: float,
        days_elapsed_in_quarter: int,
        total_days_in_quarter: int = 90
    ) -> Dict[str, Any]:
        expected_attainment_pct = round((days_elapsed_in_quarter / float(total_days_in_quarter)) * 100.0, 1)
        actual_attainment_pct = round((actual_closed_revenue / max(1.0, quarter_quota)) * 100.0, 1)
        pacing_index = round((actual_attainment_pct / max(0.1, expected_attainment_pct)) * 100.0, 1)

        projected_quarter_finish = round(actual_closed_revenue * (total_days_in_quarter / max(1, days_elapsed_in_quarter)), 2)

        return {
            "quarter_quota": quarter_quota,
            "actual_closed_revenue": actual_closed_revenue,
            "days_elapsed": days_elapsed_in_quarter,
            "expected_attainment_pct": expected_attainment_pct,
            "actual_attainment_pct": actual_attainment_pct,
            "pacing_index_pct": pacing_index,
            "projected_quarter_finish": projected_quarter_finish,
            "pacing_status": "Ahead of Plan" if pacing_index >= 110 else "On Pace" if pacing_index >= 90 else "Behind Pacing"
        }
""")

    # 3. backend/app/enterprise/security_governance/cmk_key_rotation_scheduler.py
    write_file("backend/app/enterprise/security_governance/cmk_key_rotation_scheduler.py", """from datetime import date, timedelta
from typing import Any, Dict, List, Optional

class CMKKeyRotationScheduler:
    @staticmethod
    def evaluate_key_age(keys: List[Dict[str, Any]], max_age_days: int = 90) -> List[Dict[str, Any]]:
        results = []
        today = date.today()

        for k in keys:
            created_str = k.get("created_date", today.isoformat())
            created_date = date.fromisoformat(created_str)
            age = (today - created_date).days
            needs_rotation = age >= max_age_days

            results.append({
                "key_id": k.get("id"),
                "key_alias": k.get("alias"),
                "age_days": age,
                "max_allowed_age": max_age_days,
                "is_rotation_due": needs_rotation,
                "status": "ROTATION_REQUIRED" if needs_rotation else "ACTIVE_COMPLIANT"
            })

        return results
""")

    # 4. frontend/src/enterprise/EnterpriseChannelSynergyMatrix.tsx
    write_file("frontend/src/enterprise/EnterpriseChannelSynergyMatrix.tsx", """import React, { useState } from "react";
import { TrendingUp, Layers, CheckCircle2, ArrowRight } from "lucide-react";

export const EnterpriseChannelSynergyMatrix: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Layers className="w-5 h-5 text-emerald-400" />
            Multi-Touch Marketing Synergy & Lift Matrix
          </h3>
          <p className="text-xs text-slate-400">Conversion velocity comparison between single-channel vs omnichannel buyer journeys</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          +14.2% Synergy Lift
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Single Touch Conversion</span>
          <div className="text-2xl font-bold text-slate-300">12.4%</div>
          <span className="text-[10px] text-slate-500">Search or Ad Only</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Omnichannel Conversion</span>
          <div className="text-2xl font-bold text-emerald-400">26.6%</div>
          <span className="text-[10px] text-emerald-400">Search + Ad + Webinar</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Net Synergy Lift</span>
          <div className="text-2xl font-bold text-purple-400">+14.2%</div>
          <span className="text-[10px] text-purple-400">2.1x Higher Close Rate</span>
        </div>
      </div>
    </div>
  );
};
""")

    # 5. frontend/src/enterprise/EnterpriseQuotaPacingChart.tsx
    write_file("frontend/src/enterprise/EnterpriseQuotaPacingChart.tsx", """import React, { useState } from "react";
import { Target, TrendingUp, CheckCircle2 } from "lucide-react";

export const EnterpriseQuotaPacingChart: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Target className="w-5 h-5 text-emerald-400" />
            Quarterly Sales Attainment & Pacing Trajectory
          </h3>
          <p className="text-xs text-slate-400">Real-time pacing against expected linear quarter progress</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          118.5% Ahead of Plan
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Closed Revenue</span>
          <div className="text-2xl font-bold text-emerald-400">$1,850,000</div>
          <span className="text-[10px] text-slate-400">Target: $2,500,000</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Pacing Expected</span>
          <div className="text-2xl font-bold text-slate-300">62.0%</div>
          <span className="text-[10px] text-slate-500">Day 56 of 90</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Projected Finish</span>
          <div className="text-2xl font-bold text-white">$2,975,000</div>
          <span className="text-[10px] text-emerald-400">+19.0% Quota Overachievement</span>
        </div>
      </div>
    </div>
  );
};
""")

    print("Created synergy modeler, pacing modeler, CMK scheduler, and UI components.")

if __name__ == '__main__':
    run()
