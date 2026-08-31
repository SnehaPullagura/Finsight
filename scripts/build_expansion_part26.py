import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/deal_loss_reason_taxonomy.py
    write_file("backend/app/enterprise/crm_analytics/deal_loss_reason_taxonomy.py", """from typing import Any, Dict, List, Optional

class DealLossReasonTaxonomy:
    CATEGORIES = {
        "pricing": ["budget_freeze", "competitor_undercut", "payment_terms_inflexibility", "roi_unclear"],
        "product": ["missing_feature", "integration_gap", "ux_complexity", "performance_scale"],
        "timing": ["project_delayed", "leadership_change", "priority_shift", "internal_build"],
        "competition": ["legacy_vendor_lock_in", "existing_bundle_discount", "brand_preference"]
    }

    @staticmethod
    def categorize_loss_reason(raw_reason: str) -> Dict[str, Any]:
        reason_lower = raw_reason.lower().strip()
        matched_category = "other"

        for cat, sub_reasons in DealLossReasonTaxonomy.CATEGORIES.items():
            if any(sr in reason_lower for sr in sub_reasons) or cat in reason_lower:
                matched_category = cat
                break

        return {
            "raw_reason": raw_reason,
            "loss_category": matched_category,
            "is_product_gap": matched_category == "product",
            "is_pricing_friction": matched_category == "pricing"
        }
""")

    # 2. backend/app/enterprise/customer_success/product_usage_telemetry_analyzer.py
    write_file("backend/app/enterprise/customer_success/product_usage_telemetry_analyzer.py", """from typing import Any, Dict, List, Optional

class ProductUsageTelemetryAnalyzer:
    @staticmethod
    def analyze_daily_active_ratio(dau: int, mau: int) -> Dict[str, Any]:
        stickiness_pct = round((dau / max(1, mau)) * 100.0, 1)

        rating = "World-Class Stickiness" if stickiness_pct >= 40.0 else "Healthy Engagement" if stickiness_pct >= 20.0 else "Low Engagement Risk"

        return {
            "daily_active_users": dau,
            "monthly_active_users": mau,
            "dau_to_mau_stickiness_pct": stickiness_pct,
            "engagement_rating": rating,
            "is_churn_risk": stickiness_pct < 15.0
        }
""")

    # 3. backend/app/enterprise/security_governance/gdpr_consent_audit_ledger.py
    write_file("backend/app/enterprise/security_governance/gdpr_consent_audit_ledger.py", """from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class GDPRConsentAuditLedger:
    @staticmethod
    def record_consent_decision(
        contact_id: str,
        consent_type: str, # marketing_email, data_processing, analytics_cookies
        granted: bool,
        ip_address: str,
        user_agent: str
    ) -> Dict[str, Any]:
        return {
            "consent_id": f"cns_{int(datetime.now(timezone.utc).timestamp() * 1000)}",
            "contact_id": contact_id,
            "consent_type": consent_type,
            "is_consent_granted": granted,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            "compliance_proof": "VALID_GDPR_ARTICLE_7_RECORD"
        }
""")

    # 4. frontend/src/enterprise/EnterpriseProductUsageTelemetry.tsx
    write_file("frontend/src/enterprise/EnterpriseProductUsageTelemetry.tsx", """import React, { useState } from "react";
import { Activity, Users, Zap, TrendingUp, CheckCircle2 } from "lucide-react";

export const EnterpriseProductUsageTelemetry: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Activity className="w-5 h-5 text-emerald-400" />
            Product Usage Telemetry & DAU / MAU Stickiness
          </h3>
          <p className="text-xs text-slate-400">User session velocity, active feature adoption, and engagement stickiness</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Top Tier Stickiness (42.5%)
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Daily Active Users (DAU)</span>
          <div className="text-2xl font-bold text-white">4,250</div>
          <span className="text-[10px] text-emerald-400">↑ 18.2% MoM</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Monthly Active Users (MAU)</span>
          <div className="text-2xl font-bold text-white">10,000</div>
          <span className="text-[10px] text-emerald-400">↑ 12.0% MoM</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">DAU / MAU Ratio</span>
          <div className="text-2xl font-bold text-emerald-400">42.5%</div>
          <span className="text-[10px] text-slate-400">Benchmark: 20%+</span>
        </div>
      </div>
    </div>
  );
};
""")

    # 5. frontend/src/enterprise/EnterpriseGDPRConsentLedger.tsx
    write_file("frontend/src/enterprise/EnterpriseGDPRConsentLedger.tsx", """import React, { useState } from "react";
import { ShieldCheck, CheckCircle2, Lock, FileText, Search } from "lucide-react";

export const EnterpriseGDPRConsentLedger: React.FC = () => {
  const consents = [
    { contact: "alex.vance@initech.internal", type: "Data Processing (Art. 6)", status: "Granted", date: "2026-08-28 14:22:05" },
    { contact: "sarah.connor@stark.internal", type: "Marketing Communications", status: "Granted", date: "2026-08-25 09:15:30" },
    { contact: "bruce.wayne@wayne.internal", type: "Analytics & Telemetry", status: "Revoked", date: "2026-08-20 18:40:12" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            GDPR Article 7 Consent Ledger & Preference Center
          </h3>
          <p className="text-xs text-slate-400">Immutable timestamped record of customer privacy consents and revocation requests</p>
        </div>
      </div>

      <div className="space-y-3">
        {consents.map((c, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{c.contact}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">{c.type} • {c.date}</div>
            </div>
            <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${
              c.status === "Granted" ? "bg-emerald-950 text-emerald-400 border border-emerald-800" : "bg-red-950 text-red-400 border border-red-800"
            }`}>
              {c.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    print("Created loss taxonomy, telemetry analyzer, GDPR consent ledger, and UI components.")

if __name__ == '__main__':
    run()
