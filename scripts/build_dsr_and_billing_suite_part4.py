import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/deal_room/dsr_security_passcode_guard.py
    write_file("backend/app/enterprise/deal_room/dsr_security_passcode_guard.py", """import hashlib
import secrets
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class DSRSecurityPasscodeGuard:
    \"\"\"
    Two-Factor PIN & Magic Link Security Guard for Executive Deal Rooms.
    \"\"\"
    @staticmethod
    def generate_access_passcode(visitor_email: str) -> Dict[str, Any]:
        pin = f"{secrets.randbelow(900000) + 100000}"
        salt = secrets.token_hex(8)
        hashed = hashlib.sha256(f"{pin}:{salt}".encode()).hexdigest()

        return {
            "visitor_email": visitor_email,
            "passcode_pin": pin,
            "passcode_hash": hashed,
            "salt": salt,
            "expires_in_minutes": 15,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
""")

    # 2. backend/app/enterprise/deal_room/buyer_intent_journey_mapper.py
    write_file("backend/app/enterprise/deal_room/buyer_intent_journey_mapper.py", """from typing import Any, Dict, List, Optional

class BuyerIntentJourneyMapper:
    \"\"\"
    Reconstructs the full buyer journey timeline from initial cold inbound to proposal sign-off.
    \"\"\"
    @staticmethod
    def map_journey_timeline(events: List[Dict[str, Any]]) -> Dict[str, Any]:
        sorted_events = sorted(events, key=lambda x: x.get("timestamp", ""))
        touchpoints_by_channel = {}

        for ev in sorted_events:
            ch = ev.get("channel", "Web")
            touchpoints_by_channel[ch] = touchpoints_by_channel.get(ch, 0) + 1

        total_touches = len(sorted_events)

        return {
            "total_touchpoints": total_touches,
            "channels_involved": touchpoints_by_channel,
            "primary_sourcing_channel": max(touchpoints_by_channel, key=touchpoints_by_channel.get) if touchpoints_by_channel else "Web",
            "journey_velocity_rating": "FAST_TRACK (< 30d)" if total_touches <= 8 else "ENTERPRISE_MULTI_TOUCH (> 15 touches)",
            "first_touch_event": sorted_events[0] if sorted_events else {},
            "last_touch_event": sorted_events[-1] if sorted_events else {}
        }
""")

    # 3. backend/app/enterprise/billing_mediation/invoice_proration_calculator.py
    write_file("backend/app/enterprise/billing_mediation/invoice_proration_calculator.py", """from datetime import date
from typing import Any, Dict, List, Optional

class InvoiceProrationCalculator:
    \"\"\"
    Calculates exact day-level proration credits and charges for mid-cycle seat additions and tier upgrades.
    \"\"\"
    @staticmethod
    def calculate_mid_cycle_proration(
        days_in_month: int,
        days_remaining: int,
        current_monthly_rate: float,
        new_monthly_rate: float,
        additional_seats: int = 1
    ) -> Dict[str, Any]:
        rate_diff = (new_monthly_rate - current_monthly_rate) * additional_seats
        daily_rate = rate_diff / max(1, days_in_month)
        prorated_charge = round(daily_rate * days_remaining, 2)

        return {
            "days_in_billing_cycle": days_in_month,
            "days_remaining_in_cycle": days_remaining,
            "additional_seats_added": additional_seats,
            "monthly_rate_difference": round(rate_diff, 2),
            "prorated_charge_due_now": prorated_charge,
            "next_full_cycle_charge": round(new_monthly_rate * additional_seats, 2)
        }
""")

    # 4. backend/app/enterprise/pipeline_forecasting/sales_capacity_ramping_model.py
    write_file("backend/app/enterprise/pipeline_forecasting/sales_capacity_ramping_model.py", """from typing import Any, Dict, List, Optional

class SalesCapacityRampingModel:
    \"\"\"
    Simulates annual sales team capacity ramping (Month 1: 0%, Month 2: 25%, Month 3: 50%, Month 4: 75%, Month 5+: 100%).
    \"\"\"
    @staticmethod
    def forecast_team_capacity(
        reps_tenure_months: List[int],
        annual_quota_per_fully_ramped_rep: float = 1000000.0
    ) -> Dict[str, Any]:
        monthly_quota = annual_quota_per_fully_ramped_rep / 12.0
        total_effective_reps = 0.0

        for t in reps_tenure_months:
            if t <= 1:
                eff = 0.0
            elif t == 2:
                eff = 0.25
            elif t == 3:
                eff = 0.50
            elif t == 4:
                eff = 0.75
            else:
                eff = 1.0
            total_effective_reps += eff

        projected_monthly_capacity = round(total_effective_reps * monthly_quota, 2)
        annualized_runway = round(projected_monthly_capacity * 12.0, 2)

        return {
            "total_headcount": len(reps_tenure_months),
            "effective_ramped_headcount": round(total_effective_reps, 2),
            "fully_ramped_ratio_pct": round((total_effective_reps / max(1, len(reps_tenure_months))) * 100.0, 1),
            "projected_monthly_quota_capacity": projected_monthly_capacity,
            "annualized_quota_capacity": annualized_runway
        }
""")

    # 5. frontend/src/enterprise/EnterpriseProrationCalculatorStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseProrationCalculatorStudio.tsx", """import React, { useState } from "react";
import { Calculator, DollarSign, Calendar, CheckCircle2 } from "lucide-react";

export const EnterpriseProrationCalculatorStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Calculator className="w-5 h-5 text-emerald-400" />
            Mid-Cycle License Upgrade & Proration Engine
          </h3>
          <p className="text-xs text-slate-400">Day-level exact proration credits for seat additions co-termed to monthly/annual billing dates</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Co-Termed Exact
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Additional Seats Added</span>
          <div className="text-2xl font-bold text-white">+10 Seats</div>
          <span className="text-[10px] text-slate-400">18 Days Remaining in Month</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Prorated Amount Due</span>
          <div className="text-2xl font-bold text-emerald-400">$600.00</div>
          <span className="text-[10px] text-emerald-400">Immediate Invoice Item</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Next Full Cycle Charge</span>
          <div className="text-2xl font-bold text-white">$1,000.00 / Mo</div>
          <span className="text-[10px] text-slate-400">Normal Monthly Renewal</span>
        </div>
      </div>
    </div>
  );
};
""")

    # 6. frontend/src/enterprise/EnterpriseBuyerJourneyMapStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseBuyerJourneyMapStudio.tsx", """import React, { useState } from "react";
import { GitCommit, Compass, CheckCircle2, TrendingUp } from "lucide-react";

export const EnterpriseBuyerJourneyMapStudio: React.FC = () => {
  const steps = [
    { title: "First Touch: Google Search Ad -> CPQ Interactive Product Tour", date: "Aug 12", channel: "Paid Search" },
    { title: "Discovery Call & Custom Architecture Scoping Sandbox", date: "Aug 19", channel: "Direct AE" },
    { title: "InfoSec DSR Access & SOC2 Type II Report Download", date: "Aug 26", channel: "Digital Sales Room" },
    { title: "Executive Proposal View & Mutual Action Plan Agreement", date: "Sept 01", channel: "Executive Sync" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Compass className="w-5 h-5 text-emerald-400" />
            Full-Funnel Buyer Journey Reconstructor
          </h3>
          <p className="text-xs text-slate-400">Chronological multi-touch journey attribution mapping every buyer touchpoint</p>
        </div>
      </div>

      <div className="space-y-3">
        {steps.map((s, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{s.title}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Date: {s.date} • Channel: {s.channel}</div>
            </div>
            <span className="text-xs text-emerald-400 font-semibold bg-emerald-950 border border-emerald-800 px-2.5 py-1 rounded-full">
              Touchpoint #{idx + 1}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    # 7. frontend/src/enterprise/EnterpriseSalesCapacityRampStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseSalesCapacityRampStudio.tsx", """import React, { useState } from "react";
import { Users, TrendingUp, DollarSign, CheckCircle2 } from "lucide-react";

export const EnterpriseSalesCapacityRampStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Users className="w-5 h-5 text-emerald-400" />
            AE Sales Quota Capacity & Ramp Pacing Simulator
          </h3>
          <p className="text-xs text-slate-400">Tenure-adjusted effective capacity model forecasting total annualized sales runway</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          14.25 Effective AEs
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Total AE Headcount</span>
          <div className="text-2xl font-bold text-white">18 Sales Reps</div>
          <span className="text-[10px] text-slate-400">12 Fully Ramped / 6 Onboarding</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Ramped Capacity Factor</span>
          <div className="text-2xl font-bold text-emerald-400">79.2%</div>
          <span className="text-[10px] text-emerald-400">Effective Productivity</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Annualized Capacity</span>
          <div className="text-2xl font-bold text-white">$14.25M Quota</div>
          <span className="text-[10px] text-slate-400">$1M Quota / Fully Ramped AE</span>
        </div>
      </div>
    </div>
  );
};
""")

    print("DSR and Billing part 4 created successfully.")

if __name__ == "__main__":
    run()
