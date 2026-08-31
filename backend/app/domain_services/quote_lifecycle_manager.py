from datetime import date, timedelta
from typing import Any, Dict, List, Optional

class QuoteLifecycleManager:
    @staticmethod
    def validate_quote_discount_thresholds(
        line_items: List[Dict[str, Any]],
        approver_role: str = "Sales Rep"
    ) -> Dict[str, Any]:
        max_discount_found = 0.0
        requires_manager_approval = False
        requires_vp_approval = False

        for item in line_items:
            disc_pct = float(item.get("discount_percentage", 0.0))
            max_discount_found = max(max_discount_found, disc_pct)

            if disc_pct > 30.0:
                requires_vp_approval = True
            elif disc_pct > 15.0:
                requires_manager_approval = True

        status = "approved"
        if requires_vp_approval:
            status = "requires_vp_approval" if approver_role not in ["VP of Sales", "Admin"] else "approved"
        elif requires_manager_approval:
            status = "requires_manager_approval" if approver_role not in ["Sales Manager", "VP of Sales", "Admin"] else "approved"

        return {
            "max_discount_percentage": max_discount_found,
            "requires_manager_approval": requires_manager_approval,
            "requires_vp_approval": requires_vp_approval,
            "approval_status": status
        }
