"""
Leverage (Total Debt/EBITDA) & Interest Cover Headroom Analyzer
Syndicated Lending, Loan Market Association (LMA) & Agency Banking Engine for FinSight.
"""
import math
import datetime
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class FinancialCovenantHeadroomAnalyzerSyndicateStructure(BaseModel):
    facility_agreement_id: str = "SYND-LMA-2026-901"
    borrower_corporate_name: str = "Global Infrastructure Projects Ltd"
    total_facility_commitment: float = Field(default=2500000000.0, ge=0.0)
    tenure_years: float = Field(default=7.0, ge=1.0)
    base_rate_benchmark: str = "RBI_REPO_RATE"
    margin_spread_bps: float = Field(default=275.0, ge=0.0)
    mandated_lead_arranger: str = "FinSight Capital Markets"

class FinancialCovenantHeadroomAnalyzerParticipantLender(BaseModel):
    lender_bic: str
    lender_name: str
    committed_amount: float
    syndication_share_pct: float
    pro_rata_interest_share_monthly: float
    voting_power_pct: float

class FinancialCovenantHeadroomAnalyzerFacilitySummary(BaseModel):
    facility_name: str = "Leverage (Total Debt/EBITDA) & Interest Cover Headroom Analyzer"
    computed_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    total_committed_volume: float
    all_in_cost_of_borrowing_pct: float
    majority_lenders_quorum_pct: float
    is_fully_subscribed: bool
    lenders_syndicate: List[FinancialCovenantHeadroomAnalyzerParticipantLender]
    governance_covenants: List[str]

class FinancialCovenantHeadroomAnalyzerEngine:
    @classmethod
    def manage_syndicate(
        cls, s: FinancialCovenantHeadroomAnalyzerSyndicateStructure
    ) -> FinancialCovenantHeadroomAnalyzerFacilitySummary:
        tot_vol = s.total_facility_commitment
        all_in_rate = 6.50 + (s.margin_spread_bps / 100.0) # Repo 6.50% + spread
        monthly_interest = tot_vol * (all_in_rate / 100.0 / 12.0)

        # Standard 4-bank syndicate breakdown
        banks_config = [
            ("State Bank of India", 0.40),
            ("HDFC Bank Ltd", 0.25),
            ("ICICI Bank Ltd", 0.20),
            ("Axis Bank Ltd", 0.15)
        ]

        lenders: List[FinancialCovenantHeadroomAnalyzerParticipantLender] = []
        for name, pct in banks_config:
            comm = tot_vol * pct
            int_mo = monthly_interest * pct
            lenders.append(FinancialCovenantHeadroomAnalyzerParticipantLender(
                lender_bic=f"{name[:4].upper()}INBBXXX",
                lender_name=name,
                committed_amount=round(comm, 2),
                syndication_share_pct=round(pct * 100.0, 1),
                pro_rata_interest_share_monthly=round(int_mo, 2),
                voting_power_pct=round(pct * 100.0, 1)
            ))

        covenants = [
            f"Loan Market Association (LMA) standard cross-default threshold capped at 2.0% of Net Worth.",
            f"Quarterly Debt Service Coverage Ratio (DSCR) minimum covenant of 1.35x.",
            "Pari-passu charge on all movable and immovable fixed assets of the borrower."
        ]

        return FinancialCovenantHeadroomAnalyzerFacilitySummary(
            total_committed_volume=round(tot_vol, 2),
            all_in_cost_of_borrowing_pct=round(all_in_rate, 2),
            majority_lenders_quorum_pct=66.67,
            is_fully_subscribed=True,
            lenders_syndicate=lenders,
            governance_covenants=covenants
        )
