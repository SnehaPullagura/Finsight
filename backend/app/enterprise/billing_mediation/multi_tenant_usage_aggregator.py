from typing import Any, Dict, List, Optional
from collections import defaultdict

class MultiTenantUsageAggregator:
    """
    High-efficiency memory aggregator aggregating millions of raw CDR usage records
    into tenant billing line items.
    """
    @staticmethod
    def aggregate_monthly_usage(cdr_records: List[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
        tenant_usage = defaultdict(lambda: defaultdict(float))

        for cdr in cdr_records:
            tid = cdr.get("tenant_id", "default_tenant")
            metric = cdr.get("metric_name", "api_calls")
            qty = float(cdr.get("rated_quantity", 1.0))
            tenant_usage[tid][metric] += qty

        # Convert to normal dict with rounded floats
        final_dict = {}
        for t, metrics in tenant_usage.items():
            final_dict[t] = {k: round(v, 2) for k, v in metrics.items()}

        return final_dict
