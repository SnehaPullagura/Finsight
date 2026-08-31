import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class UsageCDRParser:
    """
    Usage Call Detail Record (CDR) High-Throughput Ingestion Parser:
    Parses and normalizes raw streaming usage payloads from API gateways and Kubernetes clusters.
    """
    @staticmethod
    def parse_raw_cdr_stream(raw_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        normalized = []
        for r in raw_records:
            t_id = r.get("tenant_id")
            metric = r.get("metric_name", "api_invocations")
            qty = float(r.get("quantity", 1.0))
            ts = r.get("timestamp", datetime.now(timezone.utc).isoformat())

            normalized.append({
                "cdr_id": f"cdr_{t_id}_{int(datetime.now(timezone.utc).timestamp() * 1000)}",
                "tenant_id": t_id,
                "metric_name": metric,
                "rated_quantity": qty,
                "event_timestamp": ts,
                "is_validated": qty > 0 and t_id is not None
            })

        return normalized
