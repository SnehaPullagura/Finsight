import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/executive_sales_rep_ramp_payback.py
    write_file("backend/app/enterprise/crm_analytics/executive_sales_rep_ramp_payback.py", """from typing import Any, Dict, List, Optional

class RepRampPaybackModeler:
    @staticmethod
    def calculate_rep_cost_payback(
        base_salary: float,
        on_target_earnings: float,
        ramp_months: int,
        gross_margin_pct: float,
        average_deal_size: float,
        deals_closed_per_month_post_ramp: float
    ) -> Dict[str, Any]:
        fully_loaded_cost_during_ramp = (on_target_earnings / 12.0) * ramp_months
        monthly_gross_profit = (deals_closed_per_month_post_ramp * average_deal_size) * (gross_margin_pct / 100.0)

        payback_months = round(fully_loaded_cost_during_ramp / max(1.0, monthly_gross_profit), 1)

        return {
            "fully_loaded_ramp_investment": round(fully_loaded_cost_during_ramp, 2),
            "monthly_post_ramp_gross_profit": round(monthly_gross_profit, 2),
            "ramp_investment_payback_months": payback_months,
            "rep_roi_status": "Highly Productive (< 6 Mo)" if payback_months <= 6.0 else "Healthy (6-12 Mo)" if payback_months <= 12.0 else "Prolonged Payback (> 12 Mo)"
        }
""")

    # 2. backend/app/enterprise/security_governance/database_field_encryption_verifier.py
    write_file("backend/app/enterprise/security_governance/database_field_encryption_verifier.py", """from typing import Any, Dict, List, Optional

class DatabaseFieldEncryptionVerifier:
    @staticmethod
    def audit_encrypted_columns(database_tables: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_columns_checked = 0
        encrypted_compliant = 0
        violations = []

        for tbl in database_tables:
            tname = tbl.get("table_name")
            cols = tbl.get("sensitive_columns", [])
            for c in cols:
                total_columns_checked += 1
                if c.get("is_encrypted_at_rest"):
                    encrypted_compliant += 1
                else:
                    violations.append(f"{tname}.{c.get('column_name')}")

        compliance_pct = round((encrypted_compliant / max(1, total_columns_checked)) * 100.0, 1)

        return {
            "total_sensitive_columns_audited": total_columns_checked,
            "encrypted_compliant_columns": encrypted_compliant,
            "compliance_percentage": compliance_pct,
            "unencrypted_violations": violations,
            "soc2_cc6_compliant": len(violations) == 0
        }
""")

    # 3. frontend/src/enterprise/EnterpriseRampPaybackMatrix.tsx
    write_file("frontend/src/enterprise/EnterpriseRampPaybackMatrix.tsx", """import React, { useState } from "react";
import { TrendingUp, Users, DollarSign, Award, CheckCircle2 } from "lucide-react";

export const EnterpriseRampPaybackMatrix: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <DollarSign className="w-5 h-5 text-emerald-400" />
            Sales Rep Ramp Cost Payback & ROI Modeler
          </h3>
          <p className="text-xs text-slate-400">Calculate months required for ramped rep gross profit to amortize initial hiring and OTE draw</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          4.8 Mo Average Payback
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Ramp Investment per Rep</span>
          <div className="text-2xl font-bold text-white">$62,500</div>
          <span className="text-[10px] text-slate-400">3.5 Months Average Ramp</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Post-Ramp Monthly GP</span>
          <div className="text-2xl font-bold text-emerald-400">$13,000</div>
          <span className="text-[10px] text-emerald-400">Based on $85k Average Deal Size</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Payback Period</span>
          <div className="text-2xl font-bold text-emerald-400">4.8 Months</div>
          <span className="text-[10px] text-slate-400">Industry Benchmark: &lt; 9 Mo</span>
        </div>
      </div>
    </div>
  );
};
""")

    # 4. frontend/src/enterprise/EnterpriseHealthClusterRadar.tsx
    write_file("frontend/src/enterprise/EnterpriseHealthClusterRadar.tsx", """import React, { useState } from "react";
import { Activity, ShieldCheck, TrendingUp, Users } from "lucide-react";

export const EnterpriseHealthClusterRadar: React.FC = () => {
  const clusters = [
    { cluster: "Champions & Advocates (Health 90+)", accounts: 48, arr: "$4.85M", share: "52.4%", color: "text-emerald-400" },
    { cluster: "Stable Adopters (Health 70-89)", accounts: 32, arr: "$2.95M", share: "31.8%", color: "text-blue-400" },
    { cluster: "Needs Nurturing (Health 50-69)", accounts: 10, arr: "$980K", share: "10.6%", color: "text-amber-400" },
    { cluster: "High Churn Risk (Health < 50)", accounts: 4, arr: "$480K", share: "5.2%", color: "text-red-400" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Activity className="w-5 h-5 text-emerald-400" />
            Customer Portfolio Health Cohort Clustering
          </h3>
          <p className="text-xs text-slate-400">Segmentation of ARR base by multi-variate telemetry health bands</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {clusters.map((c, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
            <span className="text-[10px] text-slate-400 font-semibold uppercase">{c.cluster}</span>
            <div className={`text-xl font-bold ${c.color}`}>{c.arr}</div>
            <span className="text-[10px] text-slate-500">{c.accounts} Accounts • {c.share}</span>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    print("Created ramp payback modeler, encryption verifier, and UI studios.")

if __name__ == '__main__':
    run()
