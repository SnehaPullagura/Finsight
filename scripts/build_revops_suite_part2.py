import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/territory_planning/geo_territory_optimizer.py
    write_file("backend/app/enterprise/territory_planning/geo_territory_optimizer.py", """from typing import Any, Dict, List, Optional
from collections import defaultdict

class GeoTerritoryOptimizer:
    \"\"\"
    Territory Optimizer & Territory Workload Equalization Engine:
    Balances enterprise territories across reps based on Total Addressable Market (TAM),
    account count, and historical win rates.
    \"\"\"
    @staticmethod
    def balance_territories(
        accounts: List[Dict[str, Any]],
        rep_count: int
    ) -> List[Dict[str, Any]]:
        # Sort accounts by estimated ARR potential descending
        sorted_accs = sorted(accounts, key=lambda x: float(x.get("estimated_arr_potential", 10000.0)), reverse=True)
        territories = [
            {"territory_id": f"TERR-{i+1}", "rep_index": i, "assigned_accounts": [], "total_potential_arr": 0.0}
            for i in range(max(1, rep_count))
        ]

        # Greedy balance allocation
        for acc in sorted_accs:
            arr = float(acc.get("estimated_arr_potential", 10000.0))
            # Pick territory with lowest accumulated ARR
            min_terr = min(territories, key=lambda t: t["total_potential_arr"])
            min_terr["assigned_accounts"].append({
                "account_id": acc.get("id"),
                "account_name": acc.get("name"),
                "state": acc.get("state", "CA"),
                "potential_arr": arr
            })
            min_terr["total_potential_arr"] = round(min_terr["total_potential_arr"] + arr, 2)

        # Compute balance variance
        all_arrs = [t["total_potential_arr"] for t in territories]
        avg_arr = sum(all_arrs) / len(all_arrs) if all_arrs else 0.0

        for t in territories:
            variance_pct = round(((t["total_potential_arr"] - avg_arr) / max(1.0, avg_arr)) * 100.0, 1)
            t["account_count"] = len(t["assigned_accounts"])
            t["tam_variance_from_mean_pct"] = variance_pct
            t["is_balanced"] = abs(variance_pct) <= 15.0

        return territories
""")

    # 2. backend/app/enterprise/territory_planning/account_tiering_engine.py
    write_file("backend/app/enterprise/territory_planning/account_tiering_engine.py", """from typing import Any, Dict, List, Optional

class EnterpriseAccountTieringEngine:
    \"\"\"
    Algorithmic Enterprise Account Tiering:
    Assigns Tier 1 (Strategic / Named), Tier 2 (Enterprise), and Tier 3 (Commercial)
    based on employee size, tech stack signals, funding, and revenue scale.
    \"\"\"
    @staticmethod
    def classify_account_tier(account: Dict[str, Any]) -> Dict[str, Any]:
        employees = int(account.get("employee_count", 50))
        annual_rev = float(account.get("annual_revenue", 1000000.0))
        has_enterprise_crm = bool(account.get("uses_enterprise_tech_stack", False))
        funding_m = float(account.get("total_funding_millions", 0.0))

        # Scoring index: 0 to 100
        score = 0
        if employees >= 5000:
            score += 40
        elif employees >= 1000:
            score += 30
        elif employees >= 250:
            score += 20
        else:
            score += 10

        if annual_rev >= 100000000.0: # $100M+
            score += 35
        elif annual_rev >= 25000000.0: # $25M+
            score += 25
        elif annual_rev >= 5000000.0:
            score += 15
        else:
            score += 5

        if has_enterprise_crm:
            score += 15
        if funding_m >= 50.0:
            score += 10

        if score >= 75:
            tier = "TIER_1_STRATEGIC_NAMED"
            touch_model = "Dedicated Enterprise Account Executive & Named Solutions Architect"
            cadence = "Weekly Custom Outreach & Executive Alignment"
        elif score >= 50:
            tier = "TIER_2_ENTERPRISE"
            touch_model = "Territory Account Executive & Pooled Sales Engineering"
            cadence = "Bi-Weekly Multichannel Cadence"
        else:
            tier = "TIER_3_COMMERCIAL"
            touch_model = "Inside Sales & Automated Product-Led Nurture"
            cadence = "Automated Marketing & Inbound SDR Follow-Up"

        return {
            "account_id": account.get("id"),
            "account_name": account.get("name"),
            "tier_score": score,
            "assigned_tier": tier,
            "recommended_touch_model": touch_model,
            "sales_cadence": cadence
        }
""")

    # 3. backend/app/enterprise/territory_planning/rep_workload_balancer.py
    write_file("backend/app/enterprise/territory_planning/rep_workload_balancer.py", """from typing import Any, Dict, List, Optional

class RepWorkloadCapacityBalancer:
    \"\"\"
    Monitors rep active opportunities and pipeline workload capacity.
    \"\"\"
    @staticmethod
    def audit_rep_bandwidth(
        reps_load: List[Dict[str, Any]],
        max_active_deals_threshold: int = 25
    ) -> List[Dict[str, Any]]:
        results = []
        for r in reps_load:
            name = r.get("rep_name")
            active_deals = int(r.get("active_deals_count", 0))
            active_pipe = float(r.get("active_pipeline_amount", 0.0))
            quota = float(r.get("quarterly_quota", 250000.0))

            utilization_pct = round((active_deals / max(1, max_active_deals_threshold)) * 100.0, 1)

            results.append({
                "rep_name": name,
                "active_deals_count": active_deals,
                "active_pipeline_amount": active_pipe,
                "capacity_utilization_pct": utilization_pct,
                "bandwidth_status": "OVERLOADED (> 100%)" if utilization_pct > 100.0 else "OPTIMAL_BANDWIDTH (70%-100%)" if utilization_pct >= 70.0 else "UNDERUTILIZED (< 70%)",
                "can_accept_new_inbound": utilization_pct <= 90.0
            })

        return sorted(results, key=lambda x: x["capacity_utilization_pct"], reverse=True)
""")

    # 4. backend/app/enterprise/territory_planning/named_account_conflict_resolver.py
    write_file("backend/app/enterprise/territory_planning/named_account_conflict_resolver.py", """from typing import Any, Dict, List, Optional

class NamedAccountConflictResolver:
    \"\"\"
    Resolves multi-rep territory conflicts: Parent/Subsidiary ownership,
    geographic overlap, and holding company splits.
    \"\"\"
    @staticmethod
    def resolve_overlap(
        parent_account: Dict[str, Any],
        subsidiary_account: Dict[str, Any],
        parent_owner_id: str,
        sub_owner_id: str
    ) -> Dict[str, Any]:
        pname = parent_account.get("name")
        sname = subsidiary_account.get("name")

        # Global Account Rule: Parent company rep retains strategic ownership
        # while subsidiary rep receives split credit
        return {
            "conflict_type": "PARENT_SUBSIDIARY_OVERLAP",
            "parent_account": pname,
            "subsidiary_account": sname,
            "primary_strategic_owner_id": parent_owner_id,
            "local_territory_owner_id": sub_owner_id,
            "resolution_policy": "GLOBAL_ACCOUNT_DIRECTIVE",
            "commission_split": {
                "parent_owner_credit_pct": 70.0,
                "local_owner_credit_pct": 30.0
            },
            "governance_status": "RESOLVED_AUTO_APPROVED"
        }
""")

    # 5. backend/app/enterprise/territory_planning/territory_realignment_simulator.py
    write_file("backend/app/enterprise/territory_planning/territory_realignment_simulator.py", """from typing import Any, Dict, List, Optional

class TerritoryRealignmentSimulator:
    \"\"\"
    Simulates annual sales territory realignments, calculating account reassignments,
    pipeline transfer impact, and rep quota adjustments.
    \"\"\"
    @staticmethod
    def simulate_realignment(
        current_assignments: List[Dict[str, Any]],
        proposed_assignments: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        transferred_accounts = 0
        transferred_arr = 0.0

        prop_map = {p["account_id"]: p["new_rep_id"] for p in proposed_assignments}

        for cur in current_assignments:
            aid = cur.get("account_id")
            old_rep = cur.get("current_rep_id")
            arr = float(cur.get("account_arr", 0.0))

            if aid in prop_map and prop_map[aid] != old_rep:
                transferred_accounts += 1
                transferred_arr += arr

        disruption_index = round((transferred_accounts / max(1, len(current_assignments))) * 100.0, 1)

        return {
            "total_accounts_analyzed": len(current_assignments),
            "accounts_transferred": transferred_accounts,
            "total_pipeline_transferred": round(transferred_arr, 2),
            "territory_disruption_index_pct": disruption_index,
            "feasibility": "LOW_DISRUPTION (< 20%)" if disruption_index <= 20.0 else "MODERATE_DISRUPTION (20%-40%)" if disruption_index <= 40.0 else "HIGH_DISRUPTION (> 40%)"
        }
""")

    print("Territory planning suite created successfully.")

if __name__ == "__main__":
    run()
