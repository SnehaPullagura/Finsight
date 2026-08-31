from typing import Any, Dict, List, Optional

class InvoiceLineItemCompiler:
    """
    Compiles base subscription fees, overage items, and professional service charges into itemized PDF-ready structures.
    """
    @staticmethod
    def compile_invoice_lines(
        base_subscription: Dict[str, Any],
        usage_overages: List[Dict[str, Any]],
        applied_credits: float = 0.0
    ) -> Dict[str, Any]:
        line_items = [
            {
                "description": f"Subscription License: {base_subscription.get('plan_name', 'Enterprise Plan')}",
                "amount": float(base_subscription.get("amount", 0.0)),
                "type": "RECURRING_BASE"
            }
        ]

        overage_total = 0.0
        for ov in usage_overages:
            amt = float(ov.get("amount", 0.0))
            overage_total += amt
            line_items.append({
                "description": f"Metered Overage: {ov.get('metric_name')} ({ov.get('quantity')} units)",
                "amount": amt,
                "type": "USAGE_OVERAGE"
            })

        subtotal = float(base_subscription.get("amount", 0.0)) + overage_total
        net_total = max(0.0, subtotal - applied_credits)

        return {
            "line_items_count": len(line_items),
            "line_items": line_items,
            "subtotal": round(subtotal, 2),
            "credits_applied": round(applied_credits, 2),
            "net_invoice_total": round(net_total, 2),
            "payment_due_terms": "Net 30 Days"
        }
