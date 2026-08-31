from datetime import date
from typing import Any, Dict, List, Optional

class EnterpriseInvoiceDisputeHandler:
    @staticmethod
    def process_invoice_dispute(
        invoice: Dict[str, Any],
        disputed_amount: float,
        dispute_reason: str,
        claimant_id: str
    ) -> Dict[str, Any]:
        total = float(invoice.get("total_amount", 0.0))
        if disputed_amount > total:
            raise ValueError("Disputed amount cannot exceed total invoice value.")

        dispute_id = f"dsp_{invoice.get('id')[-8:]}"
        requires_vp_finance = disputed_amount >= 10000.0

        return {
            "dispute_id": dispute_id,
            "invoice_id": invoice.get("id"),
            "disputed_amount": disputed_amount,
            "dispute_reason": dispute_reason,
            "claimant_id": claimant_id,
            "status": "under_investigation",
            "requires_vp_finance_approval": requires_vp_finance,
            "adjusted_undisputed_balance": round(total - disputed_amount, 2),
            "created_date": date.today().isoformat()
        }
