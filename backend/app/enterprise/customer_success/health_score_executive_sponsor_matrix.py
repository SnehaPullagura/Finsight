from typing import Any, Dict, List, Optional

class ExecutiveSponsorAlignmentMatrix:
    @staticmethod
    def audit_sponsor_coverage(accounts: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_enterprise_accounts = len(accounts)
        covered_accounts = [a for a in accounts if a.get("executive_sponsor_email")]
        uncovered_accounts = [a for a in accounts if not a.get("executive_sponsor_email")]

        coverage_pct = round((len(covered_accounts) / max(1, total_enterprise_accounts)) * 100.0, 1)

        return {
            "total_accounts_audited": total_enterprise_accounts,
            "sponsor_aligned_count": len(covered_accounts),
            "unaligned_count": len(uncovered_accounts),
            "sponsor_coverage_percentage": coverage_pct,
            "governance_status": "EXCELLENT_COVERAGE (> 90%)" if coverage_pct >= 90.0 else "SPONSOR_GAP_NEEDS_ACTION",
            "at_risk_unaligned_accounts": [a.get("name") for a in uncovered_accounts]
        }
