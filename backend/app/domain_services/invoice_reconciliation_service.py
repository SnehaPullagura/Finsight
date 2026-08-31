from datetime import date
from typing import Any, Dict, List, Optional

class InvoiceReconciliationService:
    @staticmethod
    def reconcile_payment_against_invoice(
        invoice: Dict[str, Any],
        payment_amount: float,
        payment_reference: str
    ) -> Dict[str, Any]:
        total_due = float(invoice.get("total_amount", 0.0))
        prev_paid = float(invoice.get("amount_paid", 0.0))
        outstanding = max(0.0, round(total_due - prev_paid, 2))

        new_total_paid = round(prev_paid + payment_amount, 2)
        remaining_balance = max(0.0, round(total_due - new_total_paid, 2))

        if new_total_paid >= total_due:
            status = "paid"
        elif new_total_paid > 0:
            status = "partially_paid"
        else:
            status = "unpaid"

        return {
            "invoice_id": invoice.get("id"),
            "invoice_number": invoice.get("invoice_number"),
            "payment_applied": payment_amount,
            "payment_reference": payment_reference,
            "previous_paid": prev_paid,
            "new_total_paid": new_total_paid,
            "remaining_balance": remaining_balance,
            "new_payment_status": status
        }
