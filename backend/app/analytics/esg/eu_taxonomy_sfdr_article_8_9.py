"""
EU SFDR Article 8/9 Sustainable Finance Taxonomy Alignment Engine
Corporate ESG & Sustainability Accounting Engine for FinSight Platform.
"""
import math
import datetime
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class EuTaxonomySfdrArticle89ReportingInput(BaseModel):
    reporting_entity: str = "FinSight Global Technologies"
    fiscal_year: str = "FY 2026-27"
    electricity_kwh_annual: float = Field(default=450000.0, ge=0.0)
    fuel_diesel_litres_annual: float = Field(default=12000.0, ge=0.0)
    business_travel_passenger_km: float = Field(default=850000.0, ge=0.0)
    data_center_cloud_compute_vcu: float = Field(default=120000.0, ge=0.0)
    renewable_energy_share_pct: float = Field(default=42.5, ge=0.0, le=100.0)

class EuTaxonomySfdrArticle89EmissionsPillar(BaseModel):
    pillar_name: str
    emissions_metric_tonnes_co2e: float
    percentage_of_total: float
    decarbonization_target_2030: float

class EuTaxonomySfdrArticle89SustainabilityReport(BaseModel):
    disclosure_framework: str = "EU SFDR Article 8/9 Sustainable Finance Taxonomy Alignment Engine"
    computed_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    total_gross_emissions_tco2e: float
    carbon_intensity_per_crore_revenue: float
    esg_composite_rating: str # AAA, AA, A, BBB, BB, B, CCC
    pillars: List[EuTaxonomySfdrArticle89EmissionsPillar]
    decarbonization_milestones: List[str]

class EuTaxonomySfdrArticle89Engine:
    @classmethod
    def generate_sustainability_disclosure(
        cls, inp: EuTaxonomySfdrArticle89ReportingInput
    ) -> EuTaxonomySfdrArticle89SustainabilityReport:
        # Standard CEA & DEFRA emission factors:
        # Diesel: ~2.68 kg CO2e / litre
        # Grid Electricity: ~0.82 kg CO2e / kWh (non-renewable portion)
        # Air Travel: ~0.15 kg CO2e / km
        
        scope1 = (inp.fuel_diesel_litres_annual * 2.68) / 1000.0
        grid_kwh = inp.electricity_kwh_annual * (1.0 - (inp.renewable_energy_share_pct / 100.0))
        scope2 = (grid_kwh * 0.82) / 1000.0
        scope3 = (inp.business_travel_passenger_km * 0.15 + inp.data_center_cloud_compute_vcu * 0.05) / 1000.0
        
        total_tco2e = scope1 + scope2 + scope3

        pillars = [
            EuTaxonomySfdrArticle89EmissionsPillar(
                pillar_name="Scope 1 (Direct Stationary & Mobile Combustion)",
                emissions_metric_tonnes_co2e=round(scope1, 2),
                percentage_of_total=round((scope1 / max(0.01, total_tco2e)) * 100.0, 1),
                decarbonization_target_2030=round(scope1 * 0.50, 2)
            ),
            EuTaxonomySfdrArticle89EmissionsPillar(
                pillar_name="Scope 2 (Indirect Grid Electricity & Cooling)",
                emissions_metric_tonnes_co2e=round(scope2, 2),
                percentage_of_total=round((scope2 / max(0.01, total_tco2e)) * 100.0, 1),
                decarbonization_target_2030=0.0
            ),
            EuTaxonomySfdrArticle89EmissionsPillar(
                pillar_name="Scope 3 (Value Chain, Travel & Cloud Computing)",
                emissions_metric_tonnes_co2e=round(scope3, 2),
                percentage_of_total=round((scope3 / max(0.01, total_tco2e)) * 100.0, 1),
                decarbonization_target_2030=round(scope3 * 0.45, 2)
            )
        ]

        rating = "AA" if inp.renewable_energy_share_pct >= 40.0 else "A"

        return EuTaxonomySfdrArticle89SustainabilityReport(
            disclosure_framework="EU SFDR Article 8/9 Sustainable Finance Taxonomy Alignment Engine",
            total_gross_emissions_tco2e=round(total_tco2e, 2),
            carbon_intensity_per_crore_revenue=round(total_tco2e / 8.5, 2),
            esg_composite_rating=rating,
            pillars=pillars,
            decarbonization_milestones=[
                "Achieved 100% green power wheeling PPA contracts for corporate headquarters.",
                "Transition corporate transport fleet to electric vehicles (EV100 initiative).",
                "Mandate Science-Based Targets initiative (SBTi) 1.5C alignment for Tier-1 vendors."
            ]
        )
