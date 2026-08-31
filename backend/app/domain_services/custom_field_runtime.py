from typing import Any, Dict, List, Optional, Tuple

class CustomFieldRuntimeEngine:
    @staticmethod
    def validate_and_cast_custom_values(
        definitions: List[Dict[str, Any]],
        submitted_values: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], List[str]]:
        validated = {}
        errors = []

        for field_def in definitions:
            name = field_def.get("name")
            ftype = field_def.get("type", "text")
            required = field_def.get("required", False)
            raw_val = submitted_values.get(name)

            if required and (raw_val is None or raw_val == ""):
                errors.append(f"Field '{name}' is required.")
                continue

            if raw_val is None:
                continue

            if ftype == "number":
                try:
                    validated[name] = float(raw_val)
                except ValueError:
                    errors.append(f"Field '{name}' must be a valid number.")
            elif ftype == "boolean":
                validated[name] = bool(raw_val)
            else:
                validated[name] = str(raw_val)

        return validated, errors
