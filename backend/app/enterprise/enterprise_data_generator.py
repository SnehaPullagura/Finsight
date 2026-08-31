import random
import uuid
from datetime import datetime, date, timedelta
from typing import Any, Dict, List

class EnterpriseDataGenerator:
    COMPANIES = [
        {"name": "Stark Industries", "industry": "technology", "revenue": 15000000.0, "employees": 1200, "city": "New York", "country": "USA"},
        {"name": "Wayne Enterprises", "industry": "finance", "revenue": 28000000.0, "employees": 3500, "city": "Gotham", "country": "USA"},
        {"name": "Cyberdyne Systems", "industry": "technology", "revenue": 8500000.0, "employees": 650, "city": "Sunnyvale", "country": "USA"},
        {"name": "Oscorp Global", "industry": "healthcare", "revenue": 12000000.0, "employees": 900, "city": "Boston", "country": "USA"},
        {"name": "Acme Industrial", "industry": "manufacturing", "revenue": 6500000.0, "employees": 450, "city": "Chicago", "country": "USA"},
        {"name": "Initech Corporation", "industry": "technology", "revenue": 4200000.0, "employees": 280, "city": "Austin", "country": "USA"},
        {"name": "Umbrella Health", "industry": "healthcare", "revenue": 34000000.0, "employees": 4800, "city": "Raccoon City", "country": "USA"},
        {"name": "Massive Dynamic", "industry": "technology", "revenue": 19500000.0, "employees": 1600, "city": "New York", "country": "USA"}
    ]

    FIRST_NAMES = ["Alexander", "Pepper", "Lucius", "Bruce", "Tony", "Sarah", "John", "Diana", "Clark", "Peter", "Norman", "Miles", "Gwen", "Barry", "Arthur", "Victor"]
    LAST_NAMES = ["Vance", "Potts", "Fox", "Wayne", "Stark", "Connor", "Wick", "Prince", "Kent", "Parker", "Osborn", "Morales", "Stacy", "Allen", "Curry", "Stone"]
    TITLES = ["Chief Executive Officer", "Chief Technology Officer", "VP of Sales", "Director of Engineering", "Head of Procurement", "Senior Product Manager", "IT Operations Lead"]

    @staticmethod
    def generate_seed_contacts(tenant_id: str, count: int = 50) -> List[Dict[str, Any]]:
        contacts = []
        random.seed(42)

        for i in range(1, count + 1):
            fn = random.choice(EnterpriseDataGenerator.FIRST_NAMES)
            ln = random.choice(EnterpriseDataGenerator.LAST_NAMES)
            comp = random.choice(EnterpriseDataGenerator.COMPANIES)
            domain = comp["name"].lower().replace(" ", "") + ".internal"

            contacts.append({
                "id": f"cont-gen-{i:03d}",
                "tenant_id": tenant_id,
                "first_name": fn,
                "last_name": ln,
                "email": f"{fn.lower()}.{ln.lower()}{i}@{domain}",
                "phone": f"+1-555-{random.randint(100, 999):03d}-{random.randint(1000, 9999):04d}",
                "title": random.choice(EnterpriseDataGenerator.TITLES),
                "company_name": comp["name"],
                "lifecycle_stage": random.choice(["lead", "mql", "sql", "opportunity", "customer"]),
                "lead_source": random.choice(["inbound_web", "referral", "linkedin_ads", "direct_outreach", "webinar"])
            })

        return contacts

    @staticmethod
    def generate_seed_deals(tenant_id: str, contacts: List[Dict[str, Any]], count: int = 40) -> List[Dict[str, Any]]:
        deals = []
        stages = [
            {"id": "stg-disc", "name": "Discovery", "prob": 20},
            {"id": "stg-prop", "name": "Proposal", "prob": 50},
            {"id": "stg-nego", "name": "Negotiation", "prob": 80},
            {"id": "stg-won", "name": "Closed Won", "prob": 100}
        ]
        random.seed(42)

        for i in range(1, count + 1):
            contact = random.choice(contacts)
            stg = random.choice(stages)
            val = random.choice([25000, 50000, 85000, 120000, 250000, 450000, 750000])

            deals.append({
                "id": f"deal-gen-{i:03d}",
                "tenant_id": tenant_id,
                "name": f"{contact['company_name']} — Enterprise Platform License",
                "value": float(val),
                "currency": "USD",
                "probability": stg["prob"],
                "stage": stg["name"],
                "status": "won" if stg["prob"] == 100 else "open",
                "contact_email": contact["email"],
                "company_name": contact["company_name"]
            })

        return deals
