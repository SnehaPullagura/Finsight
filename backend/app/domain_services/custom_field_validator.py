import re
from typing import Any, Dict, List, Tuple

class CustomFieldValidator:
    @staticmethod
    def validate_field_value(field_def: Dict[str, Any], value: Any) -> Tuple[bool, Optional[str]]:
        field_name = field_def.get("name", "Field")
        field_type = field_def.get("type", "text")
        is_required = field_def.get("required", False)

        if is_required and (value is None or value == ""):
            return False, f"{field_name} is required."

        if value is None or value == "":
            return True, None

        if field_type == "number":
            try:
                float(value)
            except ValueError:
                return False, f"{field_name} must be a valid numeric value."

        elif field_type == "email":
            if not re.match(r"^[^@]+@[^@]+\.[^@]+$", str(value)):
                return False, f"{field_name} must be a valid email address."

        elif field_type == "select":
            allowed = field_def.get("options", [])
            if allowed and str(value) not in allowed:
                return False, f"{field_name} must be one of: {', '.join(allowed)}."

        return True, None
