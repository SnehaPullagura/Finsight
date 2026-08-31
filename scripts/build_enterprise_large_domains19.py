import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/enterprise_omnichannel_dispatcher.py
    write_file("backend/app/enterprise/enterprise_omnichannel_dispatcher.py", """import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class EnterpriseOmnichannelDispatcher:
    def __init__(self, default_sender_email: str = "notifications@clientflow.internal"):
        self.default_sender = default_sender_email
        self.dispatch_log = []

    async def dispatch_notification(
        self,
        recipient_id: str,
        channels: List[str], # email, sms, in_app, slack
        title: str,
        body: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        results = []
        timestamp = datetime.now(timezone.utc).isoformat()
        
        for ch in channels:
            delivery_id = f"del_{hashlib.md5(f'{recipient_id}_{ch}_{timestamp}'.encode()).hexdigest()[:16]}"
            result_entry = {
                "delivery_id": delivery_id,
                "recipient_id": recipient_id,
                "channel": ch,
                "title": title,
                "status": "delivered",
                "dispatched_at": timestamp
            }
            results.append(result_entry)
            self.dispatch_log.append(result_entry)

        return results
""")

    # 2. backend/app/enterprise/enterprise_data_importer.py
    write_file("backend/app/enterprise/enterprise_data_importer.py", """import csv
import io
from typing import Any, Dict, List, Tuple

class EnterpriseDataImporter:
    @staticmethod
    def process_csv_batch(
        csv_data: str,
        field_mapping: Dict[str, str],
        required_fields: List[str]
    ) -> Dict[str, Any]:
        reader = csv.DictReader(io.StringIO(csv_data.strip()))
        successful_records = []
        failed_records = []

        for row_idx, row in enumerate(reader, start=1):
            mapped_record = {}
            for src_col, target_field in field_mapping.items():
                if src_col in row:
                    mapped_record[target_field] = row[src_col].strip()

            missing = [f for f in required_fields if not mapped_record.get(f)]
            if missing:
                failed_records.append({
                    "row_number": row_idx,
                    "raw_data": row,
                    "errors": [f"Missing required field: '{m}'" for m in missing]
                })
            else:
                successful_records.append(mapped_record)

        return {
            "total_rows": len(successful_records) + len(failed_records),
            "successful_count": len(successful_records),
            "failed_count": len(failed_records),
            "records": successful_records,
            "failed_records": failed_records
        }
""")

    # 3. backend/app/enterprise/enterprise_sla_matrix.py
    write_file("backend/app/enterprise/enterprise_sla_matrix.py", """from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

class EnterpriseSLAMatrix:
    TIER_TARGETS = {
        "platinum": {"first_response_min": 15, "resolution_hours": 2},
        "gold": {"first_response_min": 60, "resolution_hours": 8},
        "silver": {"first_response_min": 240, "resolution_hours": 24},
        "standard": {"first_response_min": 480, "resolution_hours": 48}
    }

    @staticmethod
    def calculate_sla_deadlines(tier: str, priority: str, created_at: datetime) -> Dict[str, Any]:
        targets = EnterpriseSLAMatrix.TIER_TARGETS.get(tier.lower(), EnterpriseSLAMatrix.TIER_TARGETS["standard"])
        
        # Priority multiplier
        multiplier = 0.5 if priority.lower() == "critical" else 0.75 if priority.lower() == "high" else 1.0

        resp_minutes = int(targets["first_response_min"] * multiplier)
        res_hours = targets["resolution_hours"] * multiplier

        resp_deadline = created_at + timedelta(minutes=resp_minutes)
        res_deadline = created_at + timedelta(hours=res_hours)

        return {
            "tier": tier,
            "priority": priority,
            "response_deadline": resp_deadline.isoformat(),
            "resolution_deadline": res_deadline.isoformat(),
            "target_response_minutes": resp_minutes,
            "target_resolution_hours": round(res_hours, 1)
        }
""")

    print("Created dispatcher, data importer, and SLA matrix.")

if __name__ == '__main__':
    run()
