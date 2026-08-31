import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_workflows/invoice_dispute_handler.py
    write_file("backend/app/enterprise/crm_workflows/invoice_dispute_handler.py", """from datetime import date
from typing import Any, Dict, List, Optional

class EnterpriseInvoiceDisputeHandler:
    @staticmethod
    def process_invoice_dispute(
        invoice: Dict[str, Any],
        disputed_amount: float,
        dispute_reason: str,
        claimant_id: str
    ) -> Dict[str, Any]:
        total = float(invoice.get("total_amount", 0.0))
        if disputed_amount > total:
            raise ValueError("Disputed amount cannot exceed total invoice value.")

        dispute_id = f"dsp_{invoice.get('id')[-8:]}"
        requires_vp_finance = disputed_amount >= 10000.0

        return {
            "dispute_id": dispute_id,
            "invoice_id": invoice.get("id"),
            "disputed_amount": disputed_amount,
            "dispute_reason": dispute_reason,
            "claimant_id": claimant_id,
            "status": "under_investigation",
            "requires_vp_finance_approval": requires_vp_finance,
            "adjusted_undisputed_balance": round(total - disputed_amount, 2),
            "created_date": date.today().isoformat()
        }
""")

    # 2. backend/app/enterprise/crm_workflows/lead_routing_rule_evaluator.py
    write_file("backend/app/enterprise/crm_workflows/lead_routing_rule_evaluator.py", """from typing import Any, Dict, List, Optional

class EnterpriseLeadRoutingRuleEvaluator:
    @staticmethod
    def route_lead_to_team(lead: Dict[str, Any]) -> Dict[str, Any]:
        emp = int(lead.get("employee_count", 0))
        country = (lead.get("country") or "US").upper()
        industry = (lead.get("industry") or "technology").lower()

        if emp >= 1000:
            team = "Strategic Enterprise Team"
            sla_min = 15
        elif emp >= 250:
            team = "Mid-Market Growth Team"
            sla_min = 60
        else:
            team = "Inbound SMB Team"
            sla_min = 120

        return {
            "lead_id": lead.get("id"),
            "assigned_team": team,
            "sla_response_minutes": sla_min,
            "territory_country": country,
            "industry_segment": industry
        }
""")

    # 3. backend/app/enterprise/data_warehouse/dimensional_schema_migrator.py
    write_file("backend/app/enterprise/data_warehouse/dimensional_schema_migrator.py", """from typing import Any, Dict, List

class DimensionalSchemaMigrator:
    @staticmethod
    def get_ddl_statements() -> List[str]:
        return [
            \"\"\"
            CREATE TABLE IF NOT EXISTS dim_company (
                company_key VARCHAR(64) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                industry VARCHAR(100),
                tier VARCHAR(50),
                annual_revenue NUMERIC(15, 2),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
            \"\"\",
            \"\"\"
            CREATE TABLE IF NOT EXISTS dim_contact (
                contact_key VARCHAR(64) PRIMARY KEY,
                company_key VARCHAR(64) REFERENCES dim_company(company_key),
                first_name VARCHAR(100),
                last_name VARCHAR(100),
                email VARCHAR(255) UNIQUE,
                lifecycle_stage VARCHAR(50)
            );
            \"\"\",
            \"\"\"
            CREATE TABLE IF NOT EXISTS fact_deal_snapshot (
                deal_key VARCHAR(64) PRIMARY KEY,
                company_key VARCHAR(64) REFERENCES dim_company(company_key),
                contact_key VARCHAR(64) REFERENCES dim_contact(contact_key),
                deal_amount NUMERIC(15, 2) NOT NULL,
                probability NUMERIC(5, 2),
                stage VARCHAR(100),
                is_won BOOLEAN DEFAULT FALSE,
                is_lost BOOLEAN DEFAULT FALSE,
                snapshot_date DATE NOT NULL
            );
            \"\"\"
        ]
""")

    # 4. frontend/src/enterprise/EnterpriseDataImportMapper.tsx
    write_file("frontend/src/enterprise/EnterpriseDataImportMapper.tsx", """import React, { useState } from "react";
import { UploadCloud, CheckCircle2, ArrowRight, Table, AlertCircle } from "lucide-react";

export const EnterpriseDataImportMapper: React.FC = () => {
  const [mappings, setMappings] = useState([
    { sourceHeader: "Company_Name", targetField: "company_name", sample: "Stark Industries", status: "mapped" },
    { sourceHeader: "Contact_Email", targetField: "email", sample: "tony@stark.internal", status: "mapped" },
    { sourceHeader: "Phone_Number", targetField: "phone", sample: "+1-555-0199", status: "mapped" },
    { sourceHeader: "Annual_Rev", targetField: "annual_revenue", sample: "$15,000,000", status: "mapped" }
  ]);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <UploadCloud className="w-5 h-5 text-emerald-400" />
            CRM Schema Mapping & Data Ingestion Studio
          </h3>
          <p className="text-xs text-slate-400">Map third-party CSV/Excel fields to ClientFlow CRM dimensional entities</p>
        </div>
        <button className="bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-1.5 rounded-lg text-xs font-semibold shadow-lg transition-colors">
          Execute Import Batch
        </button>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-xs text-left">
          <thead className="bg-slate-950 text-slate-400 font-semibold border-b border-slate-800">
            <tr>
              <th className="p-3">Source Column</th>
              <th className="p-3 text-center">Mapping</th>
              <th className="p-3">ClientFlow CRM Field</th>
              <th className="p-3">Sample Preview</th>
              <th className="p-3 text-right">Validation</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-white">
            {mappings.map((m, idx) => (
              <tr key={idx} className="hover:bg-slate-800/30">
                <td className="p-3 font-mono text-slate-300">{m.sourceHeader}</td>
                <td className="p-3 text-center text-slate-500"><ArrowRight className="w-4 h-4 inline" /></td>
                <td className="p-3 font-semibold text-emerald-400">{m.targetField}</td>
                <td className="p-3 text-slate-400">{m.sample}</td>
                <td className="p-3 text-right">
                  <span className="text-emerald-400 font-medium flex items-center justify-end gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5" /> Ready
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
""")

    print("Created dispute handler, lead router, schema migrator, and Data Import UI.")

if __name__ == '__main__':
    run()
