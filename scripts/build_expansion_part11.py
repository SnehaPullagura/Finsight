import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_workflows/renewal_playbook_automator.py
    write_file("backend/app/enterprise/crm_workflows/renewal_playbook_automator.py", """from datetime import date, timedelta
from typing import Any, Dict, List, Optional

class EnterpriseRenewalPlaybookAutomator:
    @staticmethod
    def generate_renewal_tasks(contract: Dict[str, Any], health_score: int) -> List[Dict[str, Any]]:
        cid = contract.get("id")
        end_date_str = contract.get("termination_date") or date.today().isoformat()
        end_date = date.fromisoformat(end_date_str)
        arr = float(contract.get("contract_value", {}).get("total_amount", 0.0))

        tasks = []
        # T-90 Days: Executive Business Review
        tasks.append({
            "contract_id": cid,
            "days_before_renewal": 90,
            "due_date": (end_date - timedelta(days=90)).isoformat(),
            "title": f"Schedule Executive Business Review (EBR) — ARR: ${arr:,.2f}",
            "priority": "high" if arr >= 100000 else "medium",
            "assigned_role": "Customer Success Manager"
        })

        # T-60 Days: Proposal & Uplift Proposal
        uplift_pct = 5.0 if health_score >= 80 else 0.0
        tasks.append({
            "contract_id": cid,
            "days_before_renewal": 60,
            "due_date": (end_date - timedelta(days=60)).isoformat(),
            "title": f"Draft Renewal Proposal with {uplift_pct}% Standard Uplift",
            "priority": "high",
            "assigned_role": "Account Executive"
        })

        # T-30 Days: Contract Execution & Legal Review
        tasks.append({
            "contract_id": cid,
            "days_before_renewal": 30,
            "due_date": (end_date - timedelta(days=30)).isoformat(),
            "title": "Secure Signed Renewal Agreement",
            "priority": "urgent",
            "assigned_role": "Account Executive"
        })

        return tasks
""")

    # 2. backend/app/enterprise/data_warehouse/gdpr_anonymizer_service.py
    write_file("backend/app/enterprise/data_warehouse/gdpr_anonymizer_service.py", """import hashlib
import uuid
from typing import Any, Dict, List, Optional

class GDPRAnonymizerService:
    @staticmethod
    def anonymize_contact_record(contact: Dict[str, Any], salt_key: str = "gdpr_crypto_salt") -> Dict[str, Any]:
        cid = contact.get("id", str(uuid.uuid4()))
        anon_hash = hashlib.sha256(f"{cid}_{salt_key}".encode()).hexdigest()[:12]

        anonymized = dict(contact)
        anonymized["first_name"] = "GDPR_ANONYMIZED"
        anonymized["last_name"] = f"USER_{anon_hash}"
        anonymized["email"] = f"erased_{anon_hash}@erasure.internal"
        anonymized["phone"] = "[REDACTED_GDPR_ART_17]"
        anonymized["title"] = "[ANONYMIZED]"
        anonymized["notes"] = "[ALL_COMMUNICATIONS_PURGED_UNDER_GDPR]"
        anonymized["is_anonymized"] = True

        return anonymized
""")

    # 3. backend/app/enterprise/event_stream/kafka_message_serializer.py
    write_file("backend/app/enterprise/event_stream/kafka_message_serializer.py", """import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict

class KafkaMessageSerializer:
    @staticmethod
    def build_event_message(topic: str, key: str, payload: Dict[str, Any], schema_version: str = "v1") -> Dict[str, Any]:
        return {
            "message_id": str(uuid.uuid4()),
            "topic": topic,
            "key": key,
            "headers": {
                "schema_version": schema_version,
                "content_type": "application/json",
                "timestamp": datetime.now(timezone.utc).isoformat()
            },
            "payload": payload
        }
""")

    # 4. frontend/src/enterprise/EnterpriseRevenueForecastMatrix.tsx
    write_file("frontend/src/enterprise/EnterpriseRevenueForecastMatrix.tsx", """import React, { useState } from "react";
import { TrendingUp, BarChart2, DollarSign, ArrowUpRight, ShieldCheck } from "lucide-react";

export const EnterpriseRevenueForecastMatrix: React.FC = () => {
  const forecastTiers = [
    { category: "Closed Won Bookings", amount: 1450000, confidence: "100%", risk: "Zero", color: "text-emerald-400" },
    { category: "Commit Forecast", amount: 620000, confidence: "90%", risk: "Low", color: "text-blue-400" },
    { category: "Best Case Scenario", amount: 480000, confidence: "60%", risk: "Moderate", color: "text-amber-400" },
    { category: "Open Pipeline", amount: 950000, confidence: "35%", risk: "High", color: "text-purple-400" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <BarChart2 className="w-5 h-5 text-emerald-400" />
            Quarterly Revenue Forecast & Weighted Commit Matrix
          </h3>
          <p className="text-xs text-slate-400">Monte Carlo weighted probability analysis with quota gap tracking</p>
        </div>
        <div className="text-right">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Quarter Target</span>
          <div className="text-xl font-bold text-white">$2,500,000</div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {forecastTiers.map((tier, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
            <span className="text-[11px] text-slate-400 font-medium">{tier.category}</span>
            <div className={`text-xl font-bold ${tier.color}`}>${tier.amount.toLocaleString()}</div>
            <div className="text-[10px] text-slate-500 flex justify-between pt-1">
              <span>Confidence: {tier.confidence}</span>
              <span>Risk: {tier.risk}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    print("Created renewal playbook, GDPR anonymizer, Kafka serializer, and Revenue Forecast UI.")

if __name__ == '__main__':
    run()
