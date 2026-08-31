from typing import Any, Dict, List, Optional
from collections import defaultdict

class RoundRobinLeadBalancer:
    def __init__(self, sales_reps: List[Dict[str, Any]]):
        self.reps = sales_reps # List of reps with id, name, max_capacity, is_active
        self.cursor = 0
        self.assignment_counts = defaultdict(int)

    def assign_lead(self, lead_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        active_reps = [r for r in self.reps if r.get("is_active", True)]
        if not active_reps:
            return None

        # Filter by capacity
        available_reps = []
        for r in active_reps:
            rid = r.get("id")
            cap = r.get("max_capacity", 50)
            if self.assignment_counts[rid] < cap:
                available_reps.append(r)

        if not available_reps:
            available_reps = active_reps # Fallback if all at capacity

        # Select next rep round-robin
        self.cursor = self.cursor % len(available_reps)
        chosen_rep = available_reps[self.cursor]
        self.cursor = (self.cursor + 1) % len(available_reps)

        rid = chosen_rep.get("id")
        self.assignment_counts[rid] += 1

        return {
            "assigned_rep_id": rid,
            "assigned_rep_name": chosen_rep.get("name"),
            "assigned_rep_email": chosen_rep.get("email"),
            "lead_id": lead_data.get("id"),
            "current_load": self.assignment_counts[rid]
        }
