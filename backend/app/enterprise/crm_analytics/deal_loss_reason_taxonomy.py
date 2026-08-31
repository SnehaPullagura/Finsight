from typing import Any, Dict, List, Optional

class DealLossReasonTaxonomy:
    CATEGORIES = {
        "pricing": ["budget_freeze", "competitor_undercut", "payment_terms_inflexibility", "roi_unclear"],
        "product": ["missing_feature", "integration_gap", "ux_complexity", "performance_scale"],
        "timing": ["project_delayed", "leadership_change", "priority_shift", "internal_build"],
        "competition": ["legacy_vendor_lock_in", "existing_bundle_discount", "brand_preference"]
    }

    @staticmethod
    def categorize_loss_reason(raw_reason: str) -> Dict[str, Any]:
        reason_lower = raw_reason.lower().strip()
        matched_category = "other"

        for cat, sub_reasons in DealLossReasonTaxonomy.CATEGORIES.items():
            if any(sr in reason_lower for sr in sub_reasons) or cat in reason_lower:
                matched_category = cat
                break

        return {
            "raw_reason": raw_reason,
            "loss_category": matched_category,
            "is_product_gap": matched_category == "product",
            "is_pricing_friction": matched_category == "pricing"
        }
