"""
LBO Returns (IRR / MoIC) & Debt Paydown Cash Sweep Engine
Corporate M&A & Strategic Valuation Module for FinSight Platform.
"""
import math
import datetime
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class LboLeveragedBuyoutDebtPaydownDealParameters(BaseModel):
    acquirer_name: str = "Acquirer Corp"
    target_name: str = "Target Tech Ltd"
    acquirer_share_price: float = Field(default=1250.0, ge=0.0)
    acquirer_shares_outstanding: float = Field(default=10000000.0, ge=1.0)
    acquirer_net_income: float = Field(default=1500000000.0, ge=0.0)
    target_share_price: float = Field(default=450.0, ge=0.0)
    target_shares_outstanding: float = Field(default=5000000.0, ge=1.0)
    target_net_income: float = Field(default=350000000.0, ge=0.0)
    offer_premium_pct: float = Field(default=25.0, ge=0.0)
    cash_consideration_pct: float = Field(default=40.0, ge=0.0, le=100.0)
    annual_pretax_synergies: float = Field(default=80000000.0, ge=0.0)
    new_debt_interest_rate_pct: float = Field(default=8.5, ge=0.0)

class LboLeveragedBuyoutDebtPaydownAccretionResult(BaseModel):
    deal_title: str = "LBO Returns (IRR / MoIC) & Debt Paydown Cash Sweep Engine"
    computed_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    standalone_acquirer_eps: float
    pro_forma_combined_eps: float
    eps_accretion_dilution_pct: float
    is_deal_eps_accretive: bool
    total_equity_purchase_price: float
    new_shares_issued_count: float
    post_deal_ownership_acquirer_pct: float
    strategic_deal_notes: List[str]

class LboLeveragedBuyoutDebtPaydownEngine:
    @classmethod
    def evaluate_transaction(
        cls, d: LboLeveragedBuyoutDebtPaydownDealParameters
    ) -> LboLeveragedBuyoutDebtPaydownAccretionResult:
        standalone_eps = d.acquirer_net_income / d.acquirer_shares_outstanding
        
        offer_px = d.target_share_price * (1.0 + (d.offer_premium_pct / 100.0))
        total_equity_val = offer_px * d.target_shares_outstanding

        cash_needed = total_equity_val * (d.cash_consideration_pct / 100.0)
        stock_needed = total_equity_val * (1.0 - (d.cash_consideration_pct / 100.0))

        new_shares = stock_needed / d.acquirer_share_price if d.acquirer_share_price > 0 else 0.0
        total_proforma_shares = d.acquirer_shares_outstanding + new_shares

        # Incremental interest after tax (25% rate)
        interest_cost_after_tax = (cash_needed * (d.new_debt_interest_rate_pct / 100.0)) * 0.75
        synergies_after_tax = d.annual_pretax_synergies * 0.75

        proforma_net_income = d.acquirer_net_income + d.target_net_income + synergies_after_tax - interest_cost_after_tax
        proforma_eps = proforma_net_income / total_proforma_shares if total_proforma_shares > 0 else standalone_eps

        eps_delta_pct = ((proforma_eps - standalone_eps) / standalone_eps) * 100.0
        is_accretive = eps_delta_pct > 0.0
        acquirer_own_pct = (d.acquirer_shares_outstanding / total_proforma_shares) * 100.0

        notes = [
            f"Transaction evaluated on Pro Forma Year-1 EPS with {abs(eps_delta_pct):.2f}% variance.",
            f"Total equity consideration of Rs. {total_equity_val:,.2f} at {d.offer_premium_pct:.1f}% acquisition premium.",
            f"Existing shareholders retain {acquirer_own_pct:.1f}% majority pro forma voting equity."
        ]

        return LboLeveragedBuyoutDebtPaydownAccretionResult(
            standalone_acquirer_eps=round(standalone_eps, 2),
            pro_forma_combined_eps=round(proforma_eps, 2),
            eps_accretion_dilution_pct=round(eps_delta_pct, 2),
            is_deal_eps_accretive=is_accretive,
            total_equity_purchase_price=round(total_equity_val, 2),
            new_shares_issued_count=round(new_shares, 0),
            post_deal_ownership_acquirer_pct=round(acquirer_own_pct, 2),
            strategic_deal_notes=notes
        )
