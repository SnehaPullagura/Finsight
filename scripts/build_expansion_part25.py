import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/deal_push_rate_analyzer.py
    write_file("backend/app/enterprise/crm_analytics/deal_push_rate_analyzer.py", """from typing import Any, Dict, List, Optional

class DealPushRateAnalyzer:
    @staticmethod
    def calculate_pipeline_push_rate(deals: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_open = len([d for d in deals if d.get("status") == "open"])
        pushed_deals = [d for d in deals if int(d.get("push_count", 0)) > 0]
        multiple_push_deals = [d for d in deals if int(d.get("push_count", 0)) >= 2]

        push_rate_pct = round((len(pushed_deals) / max(1, total_open)) * 100.0, 1)
        multiple_push_rate_pct = round((len(multiple_push_deals) / max(1, total_open)) * 100.0, 1)

        return {
            "total_open_deals": total_open,
            "pushed_deals_count": len(pushed_deals),
            "multiple_pushed_count": len(multiple_push_deals),
            "push_rate_percentage": push_rate_pct,
            "chronic_slippage_rate_percentage": multiple_push_rate_pct,
            "pipeline_hygiene_status": "Healthy" if push_rate_pct <= 20.0 else "Warning (> 20% Pushed)" if push_rate_pct <= 40.0 else "Critical Pipeline Friction"
        }
""")

    # 2. backend/app/enterprise/crm_analytics/rep_pipeline_coverage_modeler.py
    write_file("backend/app/enterprise/crm_analytics/rep_pipeline_coverage_modeler.py", """from typing import Any, Dict, List, Optional

class RepPipelineCoverageModeler:
    @staticmethod
    def calculate_rep_coverage_ratios(reps_data: List[Dict[str, Any]], target_coverage_multiple: float = 3.0) -> List[Dict[str, Any]]:
        results = []
        for r in reps_data:
            quota = float(r.get("quota_remaining", 100000.0))
            pipeline = float(r.get("open_pipeline", 0.0))
            coverage = round(pipeline / max(1.0, quota), 2)
            gap = max(0.0, round((quota * target_coverage_multiple) - pipeline, 2))

            results.append({
                "rep_id": r.get("id"),
                "rep_name": r.get("name"),
                "quota_remaining": quota,
                "open_pipeline": pipeline,
                "coverage_multiple": coverage,
                "target_coverage": target_coverage_multiple,
                "pipeline_gap_to_target": gap,
                "is_well_covered": coverage >= target_coverage_multiple
            })

        return sorted(results, key=lambda x: x["coverage_multiple"])
""")

    # 3. backend/app/enterprise/security_governance/api_key_vault_manager.py
    write_file("backend/app/enterprise/security_governance/api_key_vault_manager.py", """import secrets
import hashlib
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

class APIKeyVaultManager:
    @staticmethod
    def generate_scoped_api_key(tenant_id: str, name: str, scopes: List[str], expires_in_days: int = 90) -> Dict[str, Any]:
        raw_token = f"cfk_{secrets.token_urlsafe(32)}"
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        expires_at = datetime.now(timezone.utc) + timedelta(days=expires_in_days)

        return {
            "key_id": f"key_{token_hash[:12]}",
            "name": name,
            "tenant_id": tenant_id,
            "masked_key": f"{raw_token[:7]}...{raw_token[-4:]}",
            "raw_key_plain": raw_token, # Only returned once upon creation
            "token_hash": token_hash,
            "scopes": scopes,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "expires_at": expires_at.isoformat()
        }
""")

    # 4. frontend/src/enterprise/EnterprisePipelineCoverageChart.tsx
    write_file("frontend/src/enterprise/EnterprisePipelineCoverageChart.tsx", """import React, { useState } from "react";
import { Target, CheckCircle2, AlertTriangle, Users } from "lucide-react";

export const EnterprisePipelineCoverageChart: React.FC = () => {
  const coverage = [
    { rep: "Alex Vance", quota: "$150,000", pipe: "$540,000", multiple: "3.6x", status: "Healthy" },
    { rep: "Sarah Connor", quota: "$200,000", pipe: "$620,000", multiple: "3.1x", status: "Healthy" },
    { rep: "John Wick", quota: "$120,000", pipe: "$210,000", multiple: "1.8x", status: "At Risk" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Target className="w-5 h-5 text-emerald-400" />
            Sales Rep Pipeline Quota Coverage Ratio
          </h3>
          <p className="text-xs text-slate-400">Track 3.0x+ pipeline coverage targets across sales team members</p>
        </div>
      </div>

      <div className="space-y-3">
        {coverage.map((c, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{c.rep}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">
                Remaining Quota: {c.quota} • Open Pipeline: {c.pipe}
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="text-right">
                <span className="text-sm font-bold text-white">{c.multiple}</span>
                <span className="text-[10px] text-slate-500 block">Coverage</span>
              </div>
              <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${
                c.status === "Healthy" ? "bg-emerald-950 text-emerald-400 border border-emerald-800" : "bg-red-950 text-red-400 border border-red-800"
              }`}>
                {c.status}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    # 5. frontend/src/enterprise/EnterpriseAPIKeyVaultManager.tsx
    write_file("frontend/src/enterprise/EnterpriseAPIKeyVaultManager.tsx", """import React, { useState } from "react";
import { Key, Shield, Plus, CheckCircle2, Lock } from "lucide-react";

export const EnterpriseAPIKeyVaultManager: React.FC = () => {
  const keys = [
    { name: "Production Stripe Webhook Receiver", key: "cfk_prod_8a9...3f12", created: "2026-08-15", scopes: "billing.read, invoices.write" },
    { name: "CI/CD Deployment & Ingestion Pipeline", key: "cfk_pipe_1b2...99ee", created: "2026-08-20", scopes: "contacts.write, deals.write" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Key className="w-5 h-5 text-emerald-400" />
            API Key Vault & Scoped Access Tokens
          </h3>
          <p className="text-xs text-slate-400">Cryptographically hashed API access tokens with fine-grained endpoint permissions</p>
        </div>
        <button className="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-500 text-white px-3 py-1.5 rounded-lg text-xs font-semibold shadow transition-colors">
          <Plus className="w-4 h-4" />
          Generate Key
        </button>
      </div>

      <div className="space-y-3">
        {keys.map((k, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{k.name}</div>
              <div className="text-[11px] font-mono text-slate-400 mt-0.5">{k.key}</div>
              <div className="text-[10px] text-slate-500 mt-1">Scopes: {k.scopes}</div>
            </div>
            <span className="text-xs text-emerald-400 font-semibold flex items-center gap-1">
              <CheckCircle2 className="w-3.5 h-3.5" /> Active
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    print("Created push rate analyzer, coverage modeler, API key vault, and UI components.")

if __name__ == '__main__':
    run()
