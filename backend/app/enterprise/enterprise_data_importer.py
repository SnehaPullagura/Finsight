import csv
import io
from typing import Any, Dict, List, Tuple

class EnterpriseDataImporter:
    @staticmethod
    def process_csv_batch(
        csv_data: str,
        field_mapping: Dict[str, str],
        required_fields: List[str]
    ) -> Dict[str, Any]:
        reader = csv.DictReader(io.StringIO(csv_data.strip()))
        successful_records = []
        failed_records = []

        for row_idx, row in enumerate(reader, start=1):
            mapped_record = {}
            for src_col, target_field in field_mapping.items():
                if src_col in row:
                    mapped_record[target_field] = row[src_col].strip()

            missing = [f for f in required_fields if not mapped_record.get(f)]
            if missing:
                failed_records.append({
                    "row_number": row_idx,
                    "raw_data": row,
                    "errors": [f"Missing required field: '{m}'" for m in missing]
                })
            else:
                successful_records.append(mapped_record)

        return {
            "total_rows": len(successful_records) + len(failed_records),
            "successful_count": len(successful_records),
            "failed_count": len(failed_records),
            "records": successful_records,
            "failed_records": failed_records
        }
