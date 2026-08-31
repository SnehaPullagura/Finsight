import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/domain_services/support_desk_engine.py
    write_file("backend/app/domain_services/support_desk_engine.py", """from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

class SupportDeskEngine:
    @staticmethod
    def calculate_csat_metrics(ratings: List[int]) -> Dict[str, Any]:
        if not ratings:
            return {"average_csat": 0.0, "csat_percentage": 0.0, "response_count": 0}

        positive_count = sum(1 for r in ratings if r >= 4)
        total_count = len(ratings)
        avg = sum(ratings) / float(total_count)
        pct = (positive_count / float(total_count)) * 100.0

        return {
            "average_csat": round(avg, 2),
            "csat_percentage": round(pct, 1),
            "response_count": total_count,
            "distribution": {
                "5_stars": ratings.count(5),
                "4_stars": ratings.count(4),
                "3_stars": ratings.count(3),
                "2_stars": ratings.count(2),
                "1_star": ratings.count(1)
            }
        }
""")

    # 2. backend/app/domain_services/document_security_vault.py
    write_file("backend/app/domain_services/document_security_vault.py", """import hashlib
from typing import Any, Dict, List, Optional

class DocumentSecurityVault:
    @staticmethod
    def compute_sha256_checksum(content_bytes: bytes) -> str:
        return hashlib.sha256(content_bytes).hexdigest()

    @staticmethod
    def verify_document_integrity(content_bytes: bytes, expected_checksum: str) -> bool:
        computed = DocumentSecurityVault.compute_sha256_checksum(content_bytes)
        return computed.lower() == expected_checksum.lower()
""")

    # 3. backend/app/domain_services/custom_field_runtime.py
    write_file("backend/app/domain_services/custom_field_runtime.py", """from typing import Any, Dict, List, Optional, Tuple

class CustomFieldRuntimeEngine:
    @staticmethod
    def validate_and_cast_custom_values(
        definitions: List[Dict[str, Any]],
        submitted_values: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], List[str]]:
        validated = {}
        errors = []

        for field_def in definitions:
            name = field_def.get("name")
            ftype = field_def.get("type", "text")
            required = field_def.get("required", False)
            raw_val = submitted_values.get(name)

            if required and (raw_val is None or raw_val == ""):
                errors.append(f"Field '{name}' is required.")
                continue

            if raw_val is None:
                continue

            if ftype == "number":
                try:
                    validated[name] = float(raw_val)
                except ValueError:
                    errors.append(f"Field '{name}' must be a valid number.")
            elif ftype == "boolean":
                validated[name] = bool(raw_val)
            else:
                validated[name] = str(raw_val)

        return validated, errors
""")

    # 4. frontend/src/components/enterprise/EnterpriseCRMComponents.tsx
    write_file("frontend/src/components/enterprise/EnterpriseCRMComponents.tsx", """import React, { useState } from "react";
import { Shield, Sparkles, Filter, Database, CheckSquare, Search, Award } from "lucide-react";

export const MultiTouchAttributionView: React.FC = () => {
  const touchpoints = [
    { channel: "Google Search (Organic)", first_touch: 40, last_touch: 10, linear: 25, w_shaped: 30 },
    { channel: "LinkedIn Sponsored Ad", first_touch: 20, last_touch: 15, linear: 20, w_shaped: 25 },
    { channel: "Product Demo Webinar", first_touch: 10, last_touch: 35, linear: 30, w_shaped: 30 },
    { channel: "Direct Executive Outreach", first_touch: 30, last_touch: 40, linear: 25, w_shaped: 15 }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div>
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <Award className="w-5 h-5 text-emerald-400" />
          Multi-Touch Marketing Attribution Comparison
        </h3>
        <p className="text-xs text-slate-400">Compare pipeline revenue attribution across First Touch, Last Touch, Linear, and W-Shaped models</p>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-xs text-left">
          <thead className="bg-slate-950 text-slate-400 font-semibold border-b border-slate-800">
            <tr>
              <th className="p-3">Marketing Channel</th>
              <th className="p-3 text-right">First Touch %</th>
              <th className="p-3 text-right">Last Touch %</th>
              <th className="p-3 text-right">Linear %</th>
              <th className="p-3 text-right text-emerald-400 font-bold">W-Shaped %</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {touchpoints.map((tp, idx) => (
              <tr key={idx} className="hover:bg-slate-800/30 text-white">
                <td className="p-3 font-medium">{tp.channel}</td>
                <td className="p-3 text-right">{tp.first_touch}%</td>
                <td className="p-3 text-right">{tp.last_touch}%</td>
                <td className="p-3 text-right">{tp.linear}%</td>
                <td className="p-3 text-right text-emerald-400 font-bold">{tp.w_shaped}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
""")

    print("Created support desk, document security, custom field runtime, and EnterpriseCRMComponents.")

if __name__ == '__main__':
    run()
