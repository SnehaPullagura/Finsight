import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class ChangeDataCaptureStreamHandler:
    def __init__(self):
        self.cdc_log = []

    def capture_change(
        self,
        table_name: str,
        operation: str, # INSERT, UPDATE, DELETE
        primary_key: str,
        before_state: Optional[Dict[str, Any]],
        after_state: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        cdc_entry = {
            "cdc_id": f"cdc_{int(datetime.now(timezone.utc).timestamp() * 1000)}",
            "table_name": table_name,
            "operation": operation.upper(),
            "primary_key": primary_key,
            "before": before_state,
            "after": after_state,
            "captured_at": datetime.now(timezone.utc).isoformat()
        }
        self.cdc_log.append(cdc_entry)
        return cdc_entry
