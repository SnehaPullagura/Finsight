import hashlib
from typing import Any, Dict, List

class DataSubjectRightsEngine:
    @staticmethod
    def export_subject_data(subject_email: str, entities_map: Dict[str, List[dict]]) -> Dict[str, Any]:
        export_package = {
            "subject_identifier": subject_email,
            "gdpr_article": "Article 15 - Right of Access",
            "extracted_records": entities_map,
            "record_count": sum(len(v) for v in entities_map.values())
        }
        return export_package

    @staticmethod
    def anonymize_text(val: str) -> str:
        if not val:
            return ""
        return "ANON_" + hashlib.sha256(val.encode()).hexdigest()[:12]
