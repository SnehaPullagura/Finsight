import re
from typing import Any, Dict, List, Tuple

class FuzzyStringDistance:
    @staticmethod
    def levenshtein_ratio(s1: str, s2: str) -> float:
        s1 = s1.lower().strip()
        s2 = s2.lower().strip()
        if s1 == s2:
            return 1.0
        if not s1 or not s2:
            return 0.0

        rows = len(s1) + 1
        cols = len(s2) + 1
        dist = [[0 for _ in range(cols)] for _ in range(rows)]

        for i in range(rows):
            dist[i][0] = i
        for j in range(cols):
            dist[0][j] = j

        for i in range(1, rows):
            for j in range(1, cols):
                cost = 0 if s1[i - 1] == s2[j - 1] else 1
                dist[i][j] = min(
                    dist[i - 1][j] + 1,      # deletion
                    dist[i][j - 1] + 1,      # insertion
                    dist[i - 1][j - 1] + cost # substitution
                )

        max_len = max(len(s1), len(s2))
        return round(1.0 - (dist[rows - 1][cols - 1] / float(max_len)), 4)

class EnterpriseFuzzyDeduplicator:
    @staticmethod
    def find_duplicate_contacts(
        target_contact: Dict[str, Any],
        candidate_pool: List[Dict[str, Any]],
        threshold: float = 0.80
    ) -> List[Dict[str, Any]]:
        matches = []
        t_email = target_contact.get("email", "").lower().strip()
        t_name = f"{target_contact.get('first_name', '')} {target_contact.get('last_name', '')}".strip()

        for c in candidate_pool:
            if c.get("id") == target_contact.get("id"):
                continue

            c_email = c.get("email", "").lower().strip()
            c_name = f"{c.get('first_name', '')} {c.get('last_name', '')}".strip()

            # Exact email match
            if t_email and c_email and t_email == c_email:
                matches.append({"candidate": c, "confidence": 1.0, "match_type": "exact_email"})
                continue

            # Fuzzy name match
            ratio = FuzzyStringDistance.levenshtein_ratio(t_name, c_name)
            if ratio >= threshold:
                matches.append({"candidate": c, "confidence": ratio, "match_type": "fuzzy_name"})

        return sorted(matches, key=lambda x: x["confidence"], reverse=True)
