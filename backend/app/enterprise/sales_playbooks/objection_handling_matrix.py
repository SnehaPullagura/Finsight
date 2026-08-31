from typing import Any, Dict, List, Optional

class ObjectionHandlingMatrix:
    BATTLECARDS = {
        "price_too_high": {
            "category": "Pricing & Budget",
            "talking_points": [
                "Focus on 3-year Total Cost of Ownership (TCO) vs legacy systems",
                "Highlight automated workflow time savings (estimated 4.5 hrs/rep/week)",
                "Offer phased multi-year ramp pricing structure"
            ],
            "recommended_asset": "ROI Calculator & Forrester TEI Whitepaper"
        },
        "evaluating_salesforce": {
            "category": "Competitor Displacement",
            "talking_points": [
                "ClientFlow CRM offers 100% native multi-tenant isolation out-of-the-box",
                "Zero hidden add-on costs for CPQ, AI Copilot, and DAG Workflows",
                "Deployment takes 2 weeks vs 6-9 months for Salesforce Enterprise"
            ],
            "recommended_asset": "Head-to-Head Architecture Benchmark Report"
        },
        "security_compliance_concerns": {
            "category": "Security & Trust",
            "talking_points": [
                "Full SOC 2 Type II, HIPAA, and GDPR Article 15/17 compliance certified",
                "AES-256 field-level encryption with customer-managed keys (CMK)",
                "Immutable cryptographic audit log with SHA-256 block hashing"
            ],
            "recommended_asset": "Enterprise Security & Compliance Whitepaper"
        }
    }

    @staticmethod
    def get_battlecard(objection_key: str) -> Optional[Dict[str, Any]]:
        return ObjectionHandlingMatrix.BATTLECARDS.get(objection_key.lower())
