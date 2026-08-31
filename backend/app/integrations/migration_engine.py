import csv
import io
import json
from typing import Dict, List, Tuple

class DataMigrationEngine:
    @staticmethod
    def map_and_transform_contacts(
        raw_records: List[Dict[str, str]],
        field_mappings: Dict[str, str]
    ) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
        valid_contacts = []
        rejected_records = []

        for row in raw_records:
            transformed = {}
            for source_col, target_field in field_mappings.items():
                val = row.get(source_col, "").strip()
                if val:
                    transformed[target_field] = val

            # Validation
            if "email" in transformed and "@" in transformed["email"]:
                if "first_name" not in transformed:
                    transformed["first_name"] = transformed["email"].split("@")[0].capitalize()
                if "last_name" not in transformed:
                    transformed["last_name"] = "Contact"
                valid_contacts.append(transformed)
            else:
                rejected_records.append({"row": row, "reason": "Missing or invalid email address"})

        return valid_contacts, rejected_records

    @staticmethod
    def parse_csv_to_dicts(csv_text: str) -> List[Dict[str, str]]:
        reader = csv.DictReader(io.StringIO(csv_text.strip()))
        return list(reader)
