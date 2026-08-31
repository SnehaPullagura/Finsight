from typing import Any, Dict, List, Optional

class DSRTemplateFactory:
    """
    Pre-packaged Digital Sales Room Templates:
    - Enterprise M&A / Strategic Acquisition
    - Mid-Market Fast-Close Package
    - Security & InfoSec Heavy Procurement
    """
    TEMPLATES = {
        "ENTERPRISE_STRATEGIC": {
            "sections": ["Executive Summary", "Architecture Blueprint", "CPQ Multi-Year Quote", "SOC2 Compliance", "Mutual Action Plan"],
            "nda_required": True,
            "tam_allocation_included": True
        },
        "INFOSEC_HEAVY": {
            "sections": ["Penetration Test Summary", "ISO 27001 / SOC2 Type II", "Data Flow Architecture", "Subprocessor List", "DPA Agreement"],
            "nda_required": True,
            "tam_allocation_included": False
        },
        "FAST_TRACK": {
            "sections": ["Product Tour Video", "1-Click Standard Order Form", "Implementation Timeline"],
            "nda_required": False,
            "tam_allocation_included": False
        }
    }

    @classmethod
    def instantiate_template(cls, template_name: str, deal_context: Dict[str, Any]) -> Dict[str, Any]:
        tmpl = cls.TEMPLATES.get(template_name.upper(), cls.TEMPLATES["FAST_TRACK"])
        return {
            "template_name": template_name.upper(),
            "account_name": deal_context.get("account_name"),
            "deal_value": deal_context.get("value"),
            "included_sections": tmpl["sections"],
            "is_nda_mandated": tmpl["nda_required"],
            "includes_tam_support": tmpl["tam_allocation_included"],
            "factory_status": "INSTANTIATED_READY_TO_CUSTOMIZE"
        }
