"""
Black-Scholes-Merton and Binomial Options Valuation Engine for hedging and equity risk analytics.
"""
import math
from typing import Dict
from pydantic import BaseModel

class OptionGreeks(BaseModel):
    price: float
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float

class DerivativesPricingEngine:
    @staticmethod
    def _cnd(x: float) -> float:
        """Cumulative standard normal distribution function (Abramowitz and Stegun)."""
        b1 = 0.319381530
        b2 = -0.356563782
        b3 = 1.781477937
        b4 = -1.821255978
        b5 = 1.330274429
        p = 0.2316419
        c = 0.39894228
        if x >= 0.0:
            t = 1.0 / (1.0 + p * x)
            return 1.0 - c * math.exp(-x * x / 2.0) * t * (t * (t * (t * (t * b5 + b4) + b3) + b2) + b1)
        else:
            t = 1.0 / (1.0 - p * x)
            return c * math.exp(-x * x / 2.0) * t * (t * (t * (t * (t * b5 + b4) + b3) + b2) + b1)

    @classmethod
    def black_scholes_call(
        cls, s: float, k: float, t: float, r: float, sigma: float
    ) -> OptionGreeks:
        if t <= 0.0 or sigma <= 0.0:
            val = max(0.0, s - k)
            return OptionGreeks(price=val, delta=1.0 if s > k else 0.0, gamma=0.0, theta=0.0, vega=0.0, rho=0.0)

        d1 = (math.log(s / k) + (r + 0.5 * sigma ** 2) * t) / (sigma * math.sqrt(t))
        d2 = d1 - sigma * math.sqrt(t)

        nd1 = cls._cnd(d1)
        nd2 = cls._cnd(d2)
        pdf_d1 = (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * d1 ** 2)

        price = s * nd1 - k * math.exp(-r * t) * nd2
        delta = nd1
        gamma = pdf_d1 / (s * sigma * math.sqrt(t))
        theta = (- (s * pdf_d1 * sigma) / (2.0 * math.sqrt(t)) - r * k * math.exp(-r * t) * nd2) / 365.0
        vega = s * math.sqrt(t) * pdf_d1 / 100.0
        rho = k * t * math.exp(-r * t) * nd2 / 100.0

        return OptionGreeks(
            price=round(price, 2),
            delta=round(delta, 4),
            gamma=round(gamma, 4),
            theta=round(theta, 4),
            vega=round(vega, 4),
            rho=round(rho, 4)
        )
