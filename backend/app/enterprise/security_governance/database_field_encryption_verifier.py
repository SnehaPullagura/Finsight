from typing import Any, Dict, List, Optional

class DatabaseFieldEncryptionVerifier:
    @staticmethod
    def audit_encrypted_columns(database_tables: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_columns_checked = 0
        encrypted_compliant = 0
        violations = []

        for tbl in database_tables:
            tname = tbl.get("table_name")
            cols = tbl.get("sensitive_columns", [])
            for c in cols:
                total_columns_checked += 1
                if c.get("is_encrypted_at_rest"):
                    encrypted_compliant += 1
                else:
                    violations.append(f"{tname}.{c.get('column_name')}")

        compliance_pct = round((encrypted_compliant / max(1, total_columns_checked)) * 100.0, 1)

        return {
            "total_sensitive_columns_audited": total_columns_checked,
            "encrypted_compliant_columns": encrypted_compliant,
            "compliance_percentage": compliance_pct,
            "unencrypted_violations": violations,
            "soc2_cc6_compliant": len(violations) == 0
        }
