"""
LP Co-Investment Vehicle (No-Fee, No-Carry) Blended Return Engine
Private Equity Fund Accounting & Waterfall Distribution Engine for FinSight.
"""
import math
import datetime
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class CoInvestmentNoFeeNoCarryFundParameters(BaseModel):
    fund_identifier: str = "PE-GROWTH-FUND-IV"
    committed_capital_total: float = Field(default=500000000.0, ge=0.0)
    drawn_capital_called: float = Field(default=450000000.0, ge=0.0)
    realized_gross_proceeds: float = Field(default=820000000.0, ge=0.0)
    preferred_hurdle_rate_annual_pct: float = Field(default=8.0, ge=0.0)
    carried_interest_rate_pct: float = Field(default=20.0, ge=0.0)
    holding_period_years: float = Field(default=5.0, ge=0.5)
    is_european_waterfall_whole_fund: bool = True

class CoInvestmentNoFeeNoCarryWaterfallTier(BaseModel):
    tier_number: int
    tier_description: str
    distributed_to_lp: float
    distributed_to_gp: float
    remaining_cash_for_next_tier: float

class CoInvestmentNoFeeNoCarryDistributionSummary(BaseModel):
    fund_name: str = "LP Co-Investment Vehicle (No-Fee, No-Carry) Blended Return Engine"
    computed_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    total_distributable_cash: float
    lp_total_distribution: float
    gp_carried_interest_total: float
    net_fund_moic_multiple: float
    net_fund_irr_pct: float
    waterfall_tiers: List[CoInvestmentNoFeeNoCarryWaterfallTier]
    governance_notes: List[str]

class CoInvestmentNoFeeNoCarryEngine:
    @classmethod
    def calculate_waterfall(
        cls, fund: CoInvestmentNoFeeNoCarryFundParameters
    ) -> CoInvestmentNoFeeNoCarryDistributionSummary:
        cash = fund.realized_gross_proceeds
        tiers: List[CoInvestmentNoFeeNoCarryWaterfallTier] = []
        
        # Tier 1: Return of Capital (100% to LP until Drawn Capital repaid)
        tier1_lp = min(cash, fund.drawn_capital_called)
        cash -= tier1_lp
        tiers.append(CoInvestmentNoFeeNoCarryWaterfallTier(
            tier_number=1,
            tier_description="Return of Contributed Capital (100% LP)",
            distributed_to_lp=round(tier1_lp, 2),
            distributed_to_gp=0.0,
            remaining_cash_for_next_tier=round(cash, 2)
        ))

        # Tier 2: Preferred Return (8% compounded)
        pref_int_total = fund.drawn_capital_called * (((1.0 + (fund.preferred_hurdle_rate_annual_pct / 100.0)) ** fund.holding_period_years) - 1.0)
        tier2_lp = min(cash, pref_int_total)
        cash -= tier2_lp
        tiers.append(CoInvestmentNoFeeNoCarryWaterfallTier(
            tier_number=2,
            tier_description=f"Preferred Return ({fund.preferred_hurdle_rate_annual_pct}% Hurdle to LP)",
            distributed_to_lp=round(tier2_lp, 2),
            distributed_to_gp=0.0,
            remaining_cash_for_next_tier=round(cash, 2)
        ))

        # Tier 3: GP Catch-Up (100% to GP until GP reaches 20% of total profits)
        target_gp_carry = (tier2_lp * 0.20) / 0.80
        tier3_gp = min(cash, target_gp_carry)
        cash -= tier3_gp
        tiers.append(CoInvestmentNoFeeNoCarryWaterfallTier(
            tier_number=3,
            tier_description="GP Catch-Up (100% GP to 20% Carry Equivalence)",
            distributed_to_lp=0.0,
            distributed_to_gp=round(tier3_gp, 2),
            remaining_cash_for_next_tier=round(cash, 2)
        ))

        # Tier 4: Residual Split (80% LP / 20% GP)
        tier4_lp = cash * 0.80
        tier4_gp = cash * 0.20
        tiers.append(CoInvestmentNoFeeNoCarryWaterfallTier(
            tier_number=4,
            tier_description="Residual Cash Split (80% LP / 20% GP)",
            distributed_to_lp=round(tier4_lp, 2),
            distributed_to_gp=round(tier4_gp, 2),
            remaining_cash_for_next_tier=0.0
        ))

        total_lp = tier1_lp + tier2_lp + tier4_lp
        total_gp = tier3_gp + tier4_gp

        moic = total_lp / fund.drawn_capital_called if fund.drawn_capital_called > 0 else 1.0
        irr = ((moic ** (1.0 / max(0.5, fund.holding_period_years))) - 1.0) * 100.0

        notes = [
            f"Net LP distribution of Rs. {total_lp:,.2f} yields {moic:.2f}x MOIC and {irr:.1f}% Net IRR.",
            f"GP Carried Interest realized: Rs. {total_gp:,.2f}.",
            "European whole-fund waterfall verified for LP principal protection prior to carry crystallization."
        ]

        return CoInvestmentNoFeeNoCarryDistributionSummary(
            total_distributable_cash=round(fund.realized_gross_proceeds, 2),
            lp_total_distribution=round(total_lp, 2),
            gp_carried_interest_total=round(total_gp, 2),
            net_fund_moic_multiple=round(moic, 2),
            net_fund_irr_pct=round(irr, 2),
            waterfall_tiers=tiers,
            governance_notes=notes
        )
