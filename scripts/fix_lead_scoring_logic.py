import os
import sys
sys.path.insert(0, os.path.abspath("."))

with open("backend/app/services/lead.py", "r", encoding="utf-8") as f:
    content = f.read()

target = """    @classmethod
    def calculate_score(cls, lead: Lead, rules: List[LeadScoringRule]) -> Tuple[int, str, Dict[str, Any]]:
        total_score = 20 # Base score
        breakdown = {}

        for rule in rules:
            points = cls.evaluate_rule(lead, rule)
            if points > 0:
                total_score += points
                breakdown[rule.name] = points"""

replacement = """    @classmethod
    def calculate_score(cls, lead: Lead, rules: List[LeadScoringRule]) -> Tuple[int, str, Dict[str, Any]]:
        total_score = 20 # Base score
        breakdown = {}

        if rules:
            for rule in rules:
                points = cls.evaluate_rule(lead, rule)
                if points > 0:
                    total_score += points
                    breakdown[rule.name] = points
        else:
            # Built-in heuristic when no custom tenant rules configured
            if (lead.estimated_budget or 0) >= 50000:
                total_score += 30
                breakdown["Enterprise Budget"] = 30
            if (lead.intent_score or 0) >= 50:
                total_score += 25
                breakdown["High Intent"] = 25
            if (lead.employee_count or 0) >= 50:
                total_score += 15
                breakdown["Target Scale"] = 15"""

content = content.replace(target, replacement)

with open("backend/app/services/lead.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated LeadQualificationEngine in lead.py.")
