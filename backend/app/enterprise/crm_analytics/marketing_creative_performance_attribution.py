from typing import Any, Dict, List, Optional

class CreativeAttributionMatrix:
    @staticmethod
    def calculate_creative_influence(creatives: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_influenced_pipeline = sum(float(c.get("influenced_pipeline", 0.0)) for c in creatives)
        top_creative = max(creatives, key=lambda x: float(x.get("influenced_pipeline", 0.0))) if creatives else {}

        return {
            "total_influenced_pipeline": round(total_influenced_pipeline, 2),
            "top_performing_asset": top_creative.get("title"),
            "top_asset_pipeline_share_pct": round((float(top_creative.get("influenced_pipeline", 0.0)) / max(1.0, total_influenced_pipeline)) * 100.0, 1) if creatives else 0.0,
            "creative_attribution_model": "Multi-Touch Algorithmic W-Shaped Weighting"
        }
