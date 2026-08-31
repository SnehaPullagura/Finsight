"""
Cross-Chain Interoperability Bridge Merkle Tree Proof of Reserves
Decentralized Finance & Digital Asset Quantitative Analytics for FinSight.
"""
import math
import datetime
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class CrossChainBridgeProofOfReservesStrategyParameters(BaseModel):
    strategy_id: str = "CRYPTO-PERP-8801"
    asset_pair: str = "BTC-USDT-PERP"
    position_size_usd: float = Field(default=250000.0, ge=0.0)
    current_funding_rate_8h_pct: float = Field(default=0.035, ge=-1.0, le=1.0)
    spot_market_price_usd: float = Field(default=64500.0, ge=0.0)
    perp_market_price_usd: float = Field(default=64585.0, ge=0.0)
    leverage_multiplier: float = Field(default=3.0, ge=1.0, le=50.0)
    annualized_borrowing_rate_usd_pct: float = Field(default=6.5, ge=0.0)

class CrossChainBridgeProofOfReservesFundingInterval(BaseModel):
    interval_index: int
    interval_timestamp: str
    expected_funding_fee_usd: float
    cumulative_yield_usd: float
    annualized_apr_pct: float

class CrossChainBridgeProofOfReservesArbitrageReport(BaseModel):
    strategy_title: str = "Cross-Chain Interoperability Bridge Merkle Tree Proof of Reserves"
    computed_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    net_annualized_carry_yield_pct: float
    basis_spread_bps: float
    is_delta_neutral: bool
    estimated_monthly_income_usd: float
    liquidation_buffer_pct: float
    schedule: List[CrossChainBridgeProofOfReservesFundingInterval]
    execution_guidance: List[str]

class CrossChainBridgeProofOfReservesEngine:
    @classmethod
    def analyze_strategy(
        cls, p: CrossChainBridgeProofOfReservesStrategyParameters
    ) -> CrossChainBridgeProofOfReservesArbitrageReport:
        # Annualized funding yield = funding_8h * 3 * 365
        annual_funding_pct = p.current_funding_rate_8h_pct * 3.0 * 365.0
        basis_bps = ((p.perp_market_price_usd - p.spot_market_price_usd) / max(1.0, p.spot_market_price_usd)) * 10000.0
        
        net_apr = annual_funding_pct - p.annualized_borrowing_rate_usd_pct
        monthly_income = (p.position_size_usd * (net_apr / 100.0)) / 12.0

        today = datetime.datetime.utcnow()
        schedule: List[CrossChainBridgeProofOfReservesFundingInterval] = []
        cum_yield = 0.0

        for i in range(1, 10):
            ts = (today + datetime.timedelta(hours=i * 8)).strftime("%Y-%m-%d %H:%M")
            fee = p.position_size_usd * (p.current_funding_rate_8h_pct / 100.0)
            cum_yield += fee

            schedule.append(CrossChainBridgeProofOfReservesFundingInterval(
                interval_index=i,
                interval_timestamp=ts,
                expected_funding_fee_usd=round(fee, 2),
                cumulative_yield_usd=round(cum_yield, 2),
                annualized_apr_pct=round(annual_funding_pct, 2)
            ))

        liq_buffer = (1.0 / p.leverage_multiplier) * 100.0 * 0.85

        guidance = [
            f"Delta-neutral cash and carry basis yield projected at {net_apr:.2f}% Net APR.",
            f"Requires Spot Long of {p.position_size_usd / p.spot_market_price_usd:.4f} BTC and equal notional Short Perpetual.",
            f"Liquidation buffer safe up to {liq_buffer:.1f}% adverse spot divergence."
        ]

        return CrossChainBridgeProofOfReservesArbitrageReport(
            net_annualized_carry_yield_pct=round(net_apr, 2),
            basis_spread_bps=round(basis_bps, 2),
            is_delta_neutral=True,
            estimated_monthly_income_usd=round(monthly_income, 2),
            liquidation_buffer_pct=round(liq_buffer, 2),
            schedule=schedule,
            execution_guidance=guidance
        )
