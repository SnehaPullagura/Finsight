import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/data_pipeline_orchestrator.py
    write_file("backend/app/enterprise/data_pipeline_orchestrator.py", """import math
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Tuple

class EnterpriseDataPipelineOrchestrator:
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.pipeline_registry = {}

    def register_pipeline(self, pipeline_name: str, pipeline_config: Dict[str, Any]):
        self.pipeline_registry[pipeline_name] = {
            "config": pipeline_config,
            "status": "ready",
            "registered_at": datetime.now(timezone.utc).isoformat()
        }

    async def execute_pipeline(self, pipeline_name: str, input_dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
        if pipeline_name not in self.pipeline_registry:
            raise ValueError(f"Pipeline '{pipeline_name}' not registered.")

        start_time = datetime.now(timezone.utc)
        processed_records = []
        errors = []

        for idx, row in enumerate(input_dataset):
            try:
                transformed = self._transform_record(row)
                processed_records.append(transformed)
            except Exception as e:
                errors.append({"record_index": idx, "error": str(e)})

        execution_duration = (datetime.now(timezone.utc) - start_time).total_seconds()

        return {
            "pipeline_name": pipeline_name,
            "tenant_id": self.tenant_id,
            "total_input": len(input_dataset),
            "total_processed": len(processed_records),
            "total_errors": len(errors),
            "duration_seconds": round(execution_duration, 4),
            "errors": errors
        }

    def _transform_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        transformed = dict(record)
        if "email" in transformed:
            transformed["email"] = str(transformed["email"]).lower().strip()
        if "value" in transformed:
            transformed["value"] = round(float(transformed["value"]), 2)
        transformed["_processed_at"] = datetime.now(timezone.utc).isoformat()
        return transformed
""")

    # 2. backend/app/enterprise/customer_segmentation_cube.py
    write_file("backend/app/enterprise/customer_segmentation_cube.py", """from typing import Any, Dict, List, Optional
from collections import defaultdict

class CustomerSegmentationCube:
    @staticmethod
    def calculate_rfm_scores(customer_orders: List[Dict[str, Any]], snapshot_date: Optional[str] = None) -> List[Dict[str, Any]]:
        # Recency, Frequency, Monetary (RFM) Segmentation
        customer_groups = defaultdict(lambda: {"orders": [], "total_spent": 0.0, "last_order_days": 999})

        for order in customer_orders:
            cid = order.get("company_id") or order.get("contact_id", "anon")
            amount = float(order.get("amount", 0.0))
            days_ago = int(order.get("days_ago", 30))

            customer_groups[cid]["orders"].append(order)
            customer_groups[cid]["total_spent"] += amount
            customer_groups[cid]["last_order_days"] = min(customer_groups[cid]["last_order_days"], days_ago)

        rfm_results = []
        for cid, data in customer_groups.items():
            r_score = 5 if data["last_order_days"] <= 14 else 4 if data["last_order_days"] <= 30 else 3 if data["last_order_days"] <= 60 else 2 if data["last_order_days"] <= 90 else 1
            f_score = 5 if len(data["orders"]) >= 10 else 4 if len(data["orders"]) >= 5 else 3 if len(data["orders"]) >= 3 else 2 if len(data["orders"]) >= 2 else 1
            m_score = 5 if data["total_spent"] >= 100000 else 4 if data["total_spent"] >= 50000 else 3 if data["total_spent"] >= 20000 else 2 if data["total_spent"] >= 5000 else 1

            composite = f"{r_score}{f_score}{m_score}"
            segment = "Champions" if r_score >= 4 and f_score >= 4 and m_score >= 4 else "Loyal Customers" if f_score >= 3 else "At Risk" if r_score <= 2 and m_score >= 3 else "Hibernating"

            rfm_results.append({
                "customer_id": cid,
                "recency_days": data["last_order_days"],
                "frequency_count": len(data["orders"]),
                "monetary_total": round(data["total_spent"], 2),
                "rfm_score": composite,
                "segment": segment
            })

        return sorted(rfm_results, key=lambda x: x["monetary_total"], reverse=True)
""")

    print("Created enterprise data pipeline orchestrator and segmentation cube.")

if __name__ == '__main__':
    run()
