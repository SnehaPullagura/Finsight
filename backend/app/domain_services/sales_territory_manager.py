from typing import Any, Dict, List, Optional, Tuple

class SalesTerritory:
    def __init__(self, territory_id: str, name: str, region: str, countries: List[str], industries: List[str], assigned_reps: List[str]):
        self.territory_id = territory_id
        self.name = name
        self.region = region
        self.countries = countries
        self.industries = industries
        self.assigned_reps = assigned_reps

    def matches(self, company_country: str, company_industry: str) -> bool:
        country_match = (not self.countries) or (company_country.upper() in [c.upper() for c in self.countries])
        industry_match = (not self.industries) or (company_industry.lower() in [i.lower() for i in self.industries])
        return country_match and industry_match

class SalesTerritoryManager:
    def __init__(self, territories: List[SalesTerritory]):
        self.territories = territories

    def assign_company_to_territory(self, company: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        country = company.get("country", "")
        industry = company.get("industry", "")

        for t in self.territories:
            if t.matches(country, industry):
                return {
                    "territory_id": t.territory_id,
                    "territory_name": t.name,
                    "region": t.region,
                    "assigned_reps": t.assigned_reps
                }

        return None
