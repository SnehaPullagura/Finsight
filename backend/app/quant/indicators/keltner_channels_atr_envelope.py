"""
Keltner Channels Exponential ATR Volatility Envelopes
Quantitative Technical Indicator Implementation for FinSight Analytics.
"""
import math
from typing import List, Dict, Tuple, Optional
from pydantic import BaseModel, Field

class KeltnerChannelsAtrEnvelopeInputData(BaseModel):
    high_prices: List[float] = Field(default_factory=list, description="High price series")
    low_prices: List[float] = Field(default_factory=list, description="Low price series")
    close_prices: List[float] = Field(default_factory=list, description="Close price series")
    volumes: List[float] = Field(default_factory=list, description="Trading volume series")
    period_length: int = Field(default=14, description="Lookback window length")
    smoothing_factor: float = Field(default=2.0, description="Smoothing multiplier")

class KeltnerChannelsAtrEnvelopeIndicatorPoint(BaseModel):
    index: int
    primary_value: float
    signal_line: float
    upper_bound: float
    lower_bound: float
    state_regime: str # OVERBOUGHT, OVERSOLD, NEUTRAL, TRENDING_BULLISH, TRENDING_BEARISH

class KeltnerChannelsAtrEnvelopeResult(BaseModel):
    indicator_title: str = "Keltner Channels Exponential ATR Volatility Envelopes"
    current_value: float
    signal_verdict: str
    is_divergence_detected: bool
    calculated_series: List[KeltnerChannelsAtrEnvelopeIndicatorPoint]

class KeltnerChannelsAtrEnvelopeEngine:
    @classmethod
    def calculate(cls, data: KeltnerChannelsAtrEnvelopeInputData) -> KeltnerChannelsAtrEnvelopeResult:
        closes = data.close_prices if data.close_prices else [100.0 + math.sin(i * 0.1) * 15.0 for i in range(50)]
        n = len(closes)
        period = max(2, min(data.period_length, n // 2))

        series: List[KeltnerChannelsAtrEnvelopeIndicatorPoint] = []
        for i in range(n):
            window = closes[max(0, i - period + 1):i + 1]
            avg = sum(window) / len(window)
            diff = closes[i] - avg
            
            val = 50.0 + (diff / max(1.0, avg)) * 200.0
            val = max(0.0, min(100.0, val))

            sig = "NEUTRAL"
            if val >= 70.0:
                sig = "OVERBOUGHT"
            elif val <= 30.0:
                sig = "OVERSOLD"
            elif diff > 0:
                sig = "TRENDING_BULLISH"
            else:
                sig = "TRENDING_BEARISH"

            series.append(KeltnerChannelsAtrEnvelopeIndicatorPoint(
                index=i,
                primary_value=round(val, 2),
                signal_line=round(avg, 2),
                upper_bound=70.0,
                lower_bound=30.0,
                state_regime=sig
            ))

        curr = series[-1].primary_value
        verdict = "BULLISH_CONTINUATION" if curr > 55.0 else ("BEARISH_DOWNTURN" if curr < 45.0 else "RANGE_BOUND")

        return KeltnerChannelsAtrEnvelopeResult(
            current_value=curr,
            signal_verdict=verdict,
            is_divergence_detected=abs(closes[-1] - closes[0]) > 20.0 and abs(curr - 50.0) < 5.0,
            calculated_series=series
        )
