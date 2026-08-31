import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/executive_rule_of_forty_calculator.py
    write_file("backend/app/enterprise/crm_analytics/executive_rule_of_forty_calculator.py", """from typing import Any, Dict, List, Optional

class RuleOfFortyCalculator:
    @staticmethod
    def calculate_efficiency_score(arr_growth_rate_pct: float, fcf_margin_pct: float) -> Dict[str, Any]:
        rule_of_40_score = round(arr_growth_rate_pct + fcf_margin_pct, 1)

        rating = "Elite Venture Grade (> 50%)" if rule_of_40_score >= 50.0 else "Top Quartile SaaS (40% - 50%)" if rule_of_40_score >= 40.0 else "Sub-Scale / Growth Needed (< 40%)"

        return {
            "arr_growth_rate_percentage": arr_growth_rate_pct,
            "free_cash_flow_margin_percentage": fcf_margin_pct,
            "rule_of_40_score": rule_of_40_score,
            "is_rule_of_40_passed": rule_of_40_score >= 40.0,
            "valuation_multiple_tier": rating
        }
""")

    # 2. backend/app/enterprise/customer_success/net_revenue_retention_analyzer.py
    write_file("backend/app/enterprise/customer_success/net_revenue_retention_analyzer.py", """from typing import Any, Dict, List, Optional

class NetRevenueRetentionAnalyzer:
    @staticmethod
    def calculate_nrr_waterfall(
        beginning_arr: float,
        expansion_arr: float,
        contraction_arr: float,
        churn_arr: float
    ) -> Dict[str, Any]:
        ending_arr = beginning_arr + expansion_arr - contraction_arr - churn_arr
        nrr_pct = round((ending_arr / max(1.0, beginning_arr)) * 100.0, 1)
        gross_retention_pct = round(((beginning_arr - contraction_arr - churn_arr) / max(1.0, beginning_arr)) * 100.0, 1)

        return {
            "beginning_arr": beginning_arr,
            "expansion_arr": expansion_arr,
            "contraction_arr": contraction_arr,
            "churn_arr": churn_arr,
            "ending_arr": ending_arr,
            "net_revenue_retention_pct": nrr_pct,
            "gross_revenue_retention_pct": gross_retention_pct,
            "nrr_health": "World-Class Enterprise (> 120%)" if nrr_pct >= 120.0 else "Healthy (105% - 120%)" if nrr_pct >= 105.0 else "Leaky Bucket (< 100%)"
        }
""")

    # 3. backend/app/enterprise/security_governance/session_ip_geofencing_guard.py
    write_file("backend/app/enterprise/security_governance/session_ip_geofencing_guard.py", """from typing import Any, Dict, List, Optional

class SessionIPGeofencingGuard:
    @staticmethod
    def validate_client_ip(client_ip: str, client_country: str, allowed_countries: List[str], ip_allowlist: List[str]) -> Dict[str, Any]:
        is_ip_allowed = client_ip in ip_allowlist if ip_allowlist else True
        is_geo_allowed = client_country.upper() in [c.upper() for c in allowed_countries] if allowed_countries else True

        is_authorized = is_ip_allowed and is_geo_allowed

        return {
            "client_ip": client_ip,
            "client_country": client_country,
            "is_ip_explicitly_whitelisted": client_ip in ip_allowlist,
            "is_geographically_permitted": is_geo_allowed,
            "is_session_authorized": is_authorized,
            "action": "ALLOW_LOGIN" if is_authorized else "CHALLENGE_WITH_MFA_OR_BLOCK"
        }
""")

    # 4. frontend/src/enterprise/EnterpriseNRRRetentionWaterfall.tsx
    write_file("frontend/src/enterprise/EnterpriseNRRRetentionWaterfall.tsx", """import React, { useState } from "react";
import { TrendingUp, DollarSign, Layers, CheckCircle2 } from "lucide-react";

export const EnterpriseNRRRetentionWaterfall: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-emerald-400" />
            Net Revenue Retention (NRR) Waterfall Studio
          </h3>
          <p className="text-xs text-slate-400">Expansion, contraction, and logo churn breakdown of cohort ARR</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          124.5% NRR (Top Decile)
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Starting ARR</span>
          <div className="text-xl font-bold text-white">$10.0M</div>
          <span className="text-[10px] text-slate-500">Base Cohort</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Expansion ARR</span>
          <div className="text-xl font-bold text-emerald-400">+$2.85M</div>
          <span className="text-[10px] text-emerald-400">+28.5% Seat & Addon Upsell</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Churn & Downsell</span>
          <div className="text-xl font-bold text-red-400">-$400K</div>
          <span className="text-[10px] text-red-400">4.0% Logo Churn</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Ending ARR</span>
          <div className="text-xl font-bold text-white">$12.45M</div>
          <span className="text-[10px] text-emerald-400">Net Growth: +$2.45M</span>
        </div>
      </div>
    </div>
  );
};
""")

    # 5. frontend/src/enterprise/EnterpriseIPGeofencingStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseIPGeofencingStudio.tsx", """import React, { useState } from "react";
import { Globe, Shield, Lock, CheckCircle2, AlertTriangle } from "lucide-react";

export const EnterpriseIPGeofencingStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Globe className="w-5 h-5 text-emerald-400" />
            Zero-Trust IP Geofencing & Country Allowlisting
          </h3>
          <p className="text-xs text-slate-400">Restrict administrative access to authorized IP CIDR blocks and sovereign jurisdictions</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Zero-Trust Guard Active
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Allowed Sovereign Regions</span>
          <div className="text-xs font-bold text-white">United States (US), European Union (EU)</div>
          <span className="text-[10px] text-emerald-400">Strict Sovereignty</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Corporate VPN CIDRs</span>
          <div className="text-xs font-mono text-white">10.100.0.0/16, 172.16.0.0/12</div>
          <span className="text-[10px] text-emerald-400">Corporate Subnets</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Blocked Geo Attempts</span>
          <div className="text-xs font-bold text-slate-300">0 Breaches in 30 Days</div>
          <span className="text-[10px] text-emerald-400">100% Blocked</span>
        </div>
      </div>
    </div>
  );
};
""")

    print("Created rule of 40 calc, NRR analyzer, geofencing guard, and UI studios.")

if __name__ == '__main__':
    run()
