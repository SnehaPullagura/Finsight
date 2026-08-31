import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/sales_playbooks/deal_qualification_meddic_engine.py
    write_file("backend/app/enterprise/sales_playbooks/deal_qualification_meddic_engine.py", """from typing import Any, Dict, List, Optional

class MEDDPICCEngine:
    CRITERIA_WEIGHTS = {
        "metrics": 15,          # Quantified economic impact ($ ROI)
        "economic_buyer": 20,   # Access to budget signoff authority
        "decision_criteria": 10,# Defined technical & business requirements
        "decision_process": 10, # Clear timeline & approval steps
        "paper_process": 15,    # Legal, procurement, & security review steps
        "identify_pain": 10,    # Compelling pain & cost of inaction
        "champion": 15,         # Internal advocate with influence
        "competition": 5        # Identified competitors & differentiation
    }

    @staticmethod
    def evaluate_deal_meddic_health(evaluations: Dict[str, bool]) -> Dict[str, Any]:
        total_score = 0
        passed_criteria = []
        missing_criteria = []

        for criterion, weight in MEDDPICCEngine.CRITERIA_WEIGHTS.items():
            if evaluations.get(criterion, False):
                total_score += weight
                passed_criteria.append(criterion)
            else:
                missing_criteria.append(criterion)

        qualification_level = "Fully Qualified" if total_score >= 85 else "Partially Qualified" if total_score >= 60 else "Unqualified / High Risk"
        is_commit_ready = total_score >= 80 and evaluations.get("economic_buyer") and evaluations.get("champion")

        return {
            "total_meddic_score": total_score,
            "qualification_level": qualification_level,
            "is_commit_ready": bool(is_commit_ready),
            "passed_criteria": passed_criteria,
            "missing_criteria": missing_criteria
        }
""")

    # 2. backend/app/enterprise/sales_playbooks/objection_handling_matrix.py
    write_file("backend/app/enterprise/sales_playbooks/objection_handling_matrix.py", """from typing import Any, Dict, List, Optional

class ObjectionHandlingMatrix:
    BATTLECARDS = {
        "price_too_high": {
            "category": "Pricing & Budget",
            "talking_points": [
                "Focus on 3-year Total Cost of Ownership (TCO) vs legacy systems",
                "Highlight automated workflow time savings (estimated 4.5 hrs/rep/week)",
                "Offer phased multi-year ramp pricing structure"
            ],
            "recommended_asset": "ROI Calculator & Forrester TEI Whitepaper"
        },
        "evaluating_salesforce": {
            "category": "Competitor Displacement",
            "talking_points": [
                "ClientFlow CRM offers 100% native multi-tenant isolation out-of-the-box",
                "Zero hidden add-on costs for CPQ, AI Copilot, and DAG Workflows",
                "Deployment takes 2 weeks vs 6-9 months for Salesforce Enterprise"
            ],
            "recommended_asset": "Head-to-Head Architecture Benchmark Report"
        },
        "security_compliance_concerns": {
            "category": "Security & Trust",
            "talking_points": [
                "Full SOC 2 Type II, HIPAA, and GDPR Article 15/17 compliance certified",
                "AES-256 field-level encryption with customer-managed keys (CMK)",
                "Immutable cryptographic audit log with SHA-256 block hashing"
            ],
            "recommended_asset": "Enterprise Security & Compliance Whitepaper"
        }
    }

    @staticmethod
    def get_battlecard(objection_key: str) -> Optional[Dict[str, Any]]:
        return ObjectionHandlingMatrix.BATTLECARDS.get(objection_key.lower())
""")

    # 3. backend/app/enterprise/data_warehouse/olap_aggregation_engine.py
    write_file("backend/app/enterprise/data_warehouse/olap_aggregation_engine.py", """from typing import Any, Dict, List, Tuple
from collections import defaultdict

class OLAPAggregationEngine:
    @staticmethod
    def compute_multi_dimensional_cube(
        records: List[Dict[str, Any]],
        dimension_keys: List[str],
        metric_key: str = "value"
    ) -> List[Dict[str, Any]]:
        cube = defaultdict(float)
        counts = defaultdict(int)

        for r in records:
            dim_values = tuple(r.get(k, "Unknown") for k in dimension_keys)
            val = float(r.get(metric_key, 0.0))
            cube[dim_values] += val
            counts[dim_values] += 1

        results = []
        for dim_values, total_val in cube.items():
            entry = {dimension_keys[i]: dim_values[i] for i in range(len(dimension_keys))}
            entry[f"total_{metric_key}"] = round(total_val, 2)
            entry["record_count"] = counts[dim_values]
            entry[f"avg_{metric_key}"] = round(total_val / max(1, counts[dim_values]), 2)
            results.append(entry)

        return sorted(results, key=lambda x: x[f"total_{metric_key}"], reverse=True)
""")

    # 4. frontend/src/enterprise/EnterpriseMEDDICScorecard.tsx
    write_file("frontend/src/enterprise/EnterpriseMEDDICScorecard.tsx", """import React, { useState } from "react";
import { CheckSquare, ShieldCheck, AlertCircle, Award, CheckCircle2 } from "lucide-react";

export const EnterpriseMEDDICScorecard: React.FC = () => {
  const [criteria, setCriteria] = useState([
    { key: "metrics", label: "Metrics (Quantified Economic Impact)", weight: 15, checked: true },
    { key: "economic_buyer", label: "Economic Buyer (Access to Decision Maker)", weight: 20, checked: true },
    { key: "decision_criteria", label: "Decision Criteria (Technical & Business)", weight: 10, checked: true },
    { key: "decision_process", label: "Decision Process (Step-by-Step Approval)", weight: 10, checked: true },
    { key: "paper_process", label: "Paper Process (Legal & Procurement)", weight: 15, checked: false },
    { key: "identify_pain", label: "Identify Pain (Compelling Event & Cost of Inaction)", weight: 10, checked: true },
    { key: "champion", label: "Champion (Internal Advocate with Clout)", weight: 15, checked: true },
    { key: "competition", label: "Competition (Identified & Differentiated)", weight: 5, checked: true }
  ]);

  const totalScore = criteria.filter(c => c.checked).reduce((sum, c) => sum + c.weight, 0);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            MEDDPICC Deal Qualification Scorecard
          </h3>
          <p className="text-xs text-slate-400">Enterprise sales qualification framework to assess deal closing probability and risk</p>
        </div>
        <div className="text-right">
          <span className="text-[11px] text-slate-400 font-medium">Qualification Score</span>
          <div className="text-2xl font-bold text-emerald-400">{totalScore} / 100</div>
        </div>
      </div>

      <div className="space-y-2.5">
        {criteria.map(c => (
          <div key={c.key} className={`p-3 rounded-lg border flex items-center justify-between transition-colors ${
            c.checked ? "bg-slate-950 border-emerald-900/50" : "bg-slate-950/60 border-slate-800"
          }`}>
            <div className="flex items-center gap-3">
              <input
                type="checkbox"
                checked={c.checked}
                onChange={() => {
                  setCriteria(criteria.map(item => item.key === c.key ? { ...item, checked: !item.checked } : item));
                }}
                className="w-4 h-4 rounded text-emerald-600 focus:ring-emerald-500 bg-slate-900 border-slate-700"
              />
              <span className="text-xs font-medium text-white">{c.label}</span>
            </div>
            <span className="text-xs font-bold text-slate-400">{c.weight} pts</span>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    print("Created MEDDIC engine, battlecards, OLAP aggregator, and MEDDIC UI.")

if __name__ == '__main__':
    run()
