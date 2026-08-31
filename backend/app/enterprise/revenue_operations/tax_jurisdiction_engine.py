from typing import Any, Dict, List, Optional

class TaxJurisdictionEngine:
    """
    Enterprise Sales Tax & VAT Determination Engine with multi-state nexus support.
    """
    RATES_BY_JURISDICTION = {
        "US-CA": {"state_tax": 0.0725, "digital_goods_exempt": True, "vat_name": "Sales Tax"},
        "US-NY": {"state_tax": 0.08875, "digital_goods_exempt": False, "vat_name": "Sales Tax"},
        "US-TX": {"state_tax": 0.0825, "digital_goods_exempt": False, "vat_name": "Sales Tax (80% SaaS Taxable)"},
        "EU-DE": {"state_tax": 0.19, "digital_goods_exempt": False, "vat_name": "MwSt (VAT)"},
        "EU-FR": {"state_tax": 0.20, "digital_goods_exempt": False, "vat_name": "TVA (VAT)"},
        "UK": {"state_tax": 0.20, "digital_goods_exempt": False, "vat_name": "VAT"},
        "SG": {"state_tax": 0.09, "digital_goods_exempt": False, "vat_name": "GST"},
        "DEFAULT": {"state_tax": 0.0, "digital_goods_exempt": True, "vat_name": "Zero Tax"}
    }

    @classmethod
    def calculate_invoice_tax(
        cls,
        jurisdiction_code: str,
        subtotal: float,
        is_tax_exempt_entity: bool = False
    ) -> Dict[str, Any]:
        if is_tax_exempt_entity:
            return {
                "jurisdiction": jurisdiction_code,
                "subtotal": round(subtotal, 2),
                "tax_rate_percentage": 0.0,
                "tax_amount": 0.0,
                "total_with_tax": round(subtotal, 2),
                "exemption_status": "EXEMPT_CERTIFICATE_VERIFIED"
            }

        rule = cls.RATES_BY_JURISDICTION.get(jurisdiction_code, cls.RATES_BY_JURISDICTION["DEFAULT"])
        rate = rule["state_tax"]
        tax_val = round(subtotal * rate, 2)
        total = round(subtotal + tax_val, 2)

        return {
            "jurisdiction": jurisdiction_code,
            "tax_regime_name": rule["vat_name"],
            "subtotal": round(subtotal, 2),
            "tax_rate_percentage": round(rate * 100.0, 3),
            "tax_amount": tax_val,
            "total_with_tax": total,
            "exemption_status": "TAXABLE"
        }
