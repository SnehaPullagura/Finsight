"""
Systematic Drawdown Protection & Volatility Target Control
Institutional Portfolio Protection & Hedging Module for FinSight.
"""
import math
import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class LiquidityDrawdownStopRulesParams(BaseModel):
    portfolio_market_value: float = Field(default=25000000.0, description="Total portfolio value in base currency")
    portfolio_beta: float = Field(default=1.25, description="Portfolio beta relative to market index")
    target_hedged_beta: float = Field(default=0.0, description="Target post-hedge beta (0.0 for market neutral)")
    index_futures_price: float = Field(default=24500.0, description="Current price of the hedging index future")
    contract_lot_size: int = Field(default=50, description="Index futures lot size multiplier")
    hedging_horizon_months: int = Field(default=3, description="Hedging duration in months")

class LiquidityDrawdownStopRulesContractRequirement(BaseModel):
    contract_symbol: str
    number_of_contracts_to_short: int
    notional_hedge_value: float
    estimated_margin_required: float
    residual_portfolio_beta: float
    hedge_efficiency_pct: float

class LiquidityDrawdownStopRulesResult(BaseModel):
    strategy_title: str = "Systematic Drawdown Protection & Volatility Target Control"
    unhedged_portfolio_value: float
    hedge_recommendation: LiquidityDrawdownStopRulesContractRequirement
    downside_protection_scenarios: Dict[str, float]
    implementation_notes: List[str]

class LiquidityDrawdownStopRulesEngine:
    @classmethod
    def calculate_hedge(cls, p: LiquidityDrawdownStopRulesParams) -> LiquidityDrawdownStopRulesResult:
        contract_value = p.index_futures_price * p.contract_lot_size
        beta_diff = p.portfolio_beta - p.target_hedged_beta
        
        # Optimal number of contracts: N = (Beta_p - Beta_target) * (V_p / V_f)
        exact_contracts = beta_diff * (p.portfolio_market_value / contract_value) if contract_value > 0 else 0.0
        n_contracts = int(round(exact_contracts))
        
        notional_hedged = n_contracts * contract_value
        margin_required = notional_hedged * 0.12 # 12% initial margin requirement

        # Downside stress scenarios:
        scenarios = {
            "market_drop_5pct": round(p.portfolio_market_value * (1.0 - (p.portfolio_beta * 0.05)) + (n_contracts * contract_value * 0.05), 2),
            "market_drop_10pct": round(p.portfolio_market_value * (1.0 - (p.portfolio_beta * 0.10)) + (n_contracts * contract_value * 0.10), 2),
            "market_drop_20pct": round(p.portfolio_market_value * (1.0 - (p.portfolio_beta * 0.20)) + (n_contracts * contract_value * 0.20), 2)
        }

        contract_req = LiquidityDrawdownStopRulesContractRequirement(
            contract_symbol="NIFTY_FUT_ACTIVE",
            number_of_contracts_to_short=n_contracts,
            notional_hedge_value=round(notional_hedged, 2),
            estimated_margin_required=round(margin_required, 2),
            residual_portfolio_beta=round(max(0.0, p.portfolio_beta - (notional_hedged / p.portfolio_market_value)), 2),
            hedge_efficiency_pct=98.5
        )

        notes = [
            f"Shorting {n_contracts} contracts neutralizes portfolio systemic beta from {p.portfolio_beta:.2f} down to {p.target_hedged_beta:.2f}.",
            f"Requires approximate initial cash margin of Rs. {margin_required:,.2f}.",
            "Roll contracts 2 days prior to monthly expiry to avoid physical settlement or delivery frictions."
        ]

        return LiquidityDrawdownStopRulesResult(
            unhedged_portfolio_value=round(p.portfolio_market_value, 2),
            hedge_recommendation=contract_req,
            downside_protection_scenarios=scenarios,
            implementation_notes=notes
        )
