import math
import re
from typing import Any, Dict, List, Set, Tuple

class FuzzyDeduplicationEngine:
    @staticmethod
    def normalize_string(val: Optional[str]) -> str:
        if not val:
            return ""
        # Lowercase, remove special characters and extra whitespace
        cleaned = re.sub(r"[^a-zA-Z0-9\s]", "", val.lower())
        return re.sub(r"\s+", " ", cleaned).strip()

    @staticmethod
    def levenshtein_distance(s1: str, s2: str) -> int:
        if len(s1) < len(s2):
            return FuzzyDeduplicationEngine.levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    @staticmethod
    def similarity_ratio(s1: str, s2: str) -> float:
        n1 = FuzzyDeduplicationEngine.normalize_string(s1)
        n2 = FuzzyDeduplicationEngine.normalize_string(s2)
        if not n1 and not n2:
            return 1.0
        if not n1 or not n2:
            return 0.0
        max_len = max(len(n1), len(n2))
        dist = FuzzyDeduplicationEngine.levenshtein_distance(n1, n2)
        return round((max_len - dist) / max_len, 4)

    @staticmethod
    def find_duplicate_contacts(
        target_contact: Dict[str, Any],
        existing_contacts: List[Dict[str, Any]],
        threshold: float = 0.85
    ) -> List[Dict[str, Any]]:
        matches = []
        target_email = (target_contact.get("email") or "").lower().strip()
        target_name = f"{target_contact.get('first_name', '')} {target_contact.get('last_name', '')}".strip()
        target_phone = re.sub(r"\D", "", target_contact.get("phone") or "")

        for existing in existing_contacts:
            score = 0.0
            reasons = []

            # 1. Exact Email Match (Score 1.0)
            ex_email = (existing.get("email") or "").lower().strip()
            if target_email and ex_email and target_email == ex_email:
                score = 1.0
                reasons.append("Exact Email Match")

            # 2. Exact Phone Match
            ex_phone = re.sub(r"\D", "", existing.get("phone") or "")
            if target_phone and ex_phone and target_phone == ex_phone:
                score = max(score, 0.95)
                reasons.append("Exact Phone Match")

            # 3. Fuzzy Name Similarity
            ex_name = f"{existing.get('first_name', '')} {existing.get('last_name', '')}".strip()
            name_sim = FuzzyDeduplicationEngine.similarity_ratio(target_name, ex_name)
            if name_sim >= threshold and score < 0.90:
                score = max(score, name_sim * 0.90)
                reasons.append(f"Fuzzy Name Match ({name_sim * 100:.1f}%)")

            if score >= threshold:
                matches.append({
                    "candidate_id": existing.get("id"),
                    "matched_contact": existing,
                    "confidence_score": round(score, 2),
                    "match_reasons": reasons
                })

        return sorted(matches, key=lambda x: x["confidence_score"], reverse=True)
