import math
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
