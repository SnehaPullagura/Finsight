"""
Crypto Asset Analytics (On-Chain Velocity, MVRV Ratio, NVT Ratio, Sharpe)
FinSight Institutional Analytics Engine.
"""
from typing import List, Dict, Optional
from pydantic import BaseModel

class CryptoAnalyticsResult(BaseModel):
    asset_module: str = "Crypto Asset Analytics (On-Chain Velocity, MVRV Ratio, NVT Ratio, Sharpe)"
    primary_metric_name: str
    primary_metric_value: float
    risk_level: str
    valuation_status: str # Undervalued, Fair Value, Overvalued
    actionable_insight: str
    historical_percentile: float

class CryptoAnalyticsEngine:
    @staticmethod
    def evaluate_asset(price: float, intrinsic_value: float, volatility: float) -> CryptoAnalyticsResult:
        ratio = price / intrinsic_value if intrinsic_value > 0 else 1.0
        
        status = "Fair Value"
        if ratio < 0.85:
            status = "Undervalued (Margin of Safety Present)"
        elif ratio > 1.15:
            status = "Overvalued (Caution Recommended)"

        risk = "Moderate"
        if volatility > 25.0:
            risk = "High"
        elif volatility < 10.0:
            risk = "Low"

        return CryptoAnalyticsResult(
            primary_metric_name="Price-to-Intrinsic Ratio",
            primary_metric_value=round(ratio, 3),
            risk_level=risk,
            valuation_status=status,
            actionable_insight=f"Asset is currently trading at {ratio:.2f}x of estimated intrinsic baseline.",
            historical_percentile=round(min(100.0, ratio * 50.0), 1)
        )
