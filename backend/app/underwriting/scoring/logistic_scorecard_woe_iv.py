"""
Weight of Evidence (WoE) & Information Value (IV) Scorecard
Institutional Credit Risk Underwriting & Default Modeling Module for FinSight.
"""
import math
import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class LogisticScorecardWoeIvBorrowerProfile(BaseModel):
    borrower_id: str = "BORR-5001"
    annual_operating_revenue: float = Field(default=25000000.0, ge=0.0)
    current_total_debt: float = Field(default=10000000.0, ge=0.0)
    annual_ebitda: float = Field(default=6000000.0, ge=0.0)
    cash_and_equivalents: float = Field(default=2500000.0, ge=0.0)
    asset_volatility_pct: float = Field(default=22.0, ge=0.0)
    requested_facility_amount: float = Field(default=5000000.0, ge=0.0)
    credit_bureau_score: int = Field(default=765, ge=300, le=900)

class LogisticScorecardWoeIvRiskRating(BaseModel):
    model_name: str = "Weight of Evidence (WoE) & Information Value (IV) Scorecard"
    borrower_id: str
    internal_credit_rating: str # AAA, AA, A, BBB, BB, B, CCC, D
    probability_of_default_1yr_pct: float
    loss_given_default_pct: float
    expected_loss_amount: float
    distance_to_default_sigma: float
    underwriting_decision: str # APPROVED, REFERRED, REJECTED
    covenant_stipulations: List[str]

class LogisticScorecardWoeIvEngine:
    @classmethod
    def evaluate_credit_risk(cls, b: LogisticScorecardWoeIvBorrowerProfile) -> LogisticScorecardWoeIvRiskRating:
        # Distance to default proxy: DD = [ln(V / D) + (mu - 0.5*sigma^2)*T] / (sigma * sqrt(T))
        total_enterprise_val = b.annual_operating_revenue * 1.5
        d_ratio = total_enterprise_val / max(1.0, b.current_total_debt)
        
        sigma = b.asset_volatility_pct / 100.0
        dd_sigma = (math.log(d_ratio) + 0.05) / max(0.01, sigma) if d_ratio > 0 else 0.5

        pd_pct = max(0.05, min(25.0, 100.0 * (1.0 / (1.0 + math.exp(dd_sigma * 1.2)))))
        lgd_pct = 45.0 # Standard Basel unsecured recovery benchmark

        exp_loss = (b.requested_facility_amount * (pd_pct / 100.0) * (lgd_pct / 100.0))

        if pd_pct < 0.5:
            rating = "AAA"
            decision = "APPROVED"
        elif pd_pct < 1.5:
            rating = "AA"
            decision = "APPROVED"
        elif pd_pct < 3.0:
            rating = "A"
            decision = "APPROVED"
        elif pd_pct < 6.0:
            rating = "BBB"
            decision = "APPROVED"
        elif pd_pct < 12.0:
            rating = "BB"
            decision = "REFERRED"
        else:
            rating = "CCC"
            decision = "REJECTED"

        covenants = [
            f"Maintain Minimum Debt Service Coverage Ratio (DSCR) of 1.35x.",
            f"Total Debt to EBITDA ratio capped at 3.00x.",
            "Quarterly submission of audited bank statement reconciliations and GST returns."
        ]

        return LogisticScorecardWoeIvRiskRating(
            borrower_id=b.borrower_id,
            internal_credit_rating=rating,
            probability_of_default_1yr_pct=round(pd_pct, 2),
            loss_given_default_pct=round(lgd_pct, 2),
            expected_loss_amount=round(exp_loss, 2),
            distance_to_default_sigma=round(dd_sigma, 2),
            underwriting_decision=decision,
            covenant_stipulations=covenants
        )
