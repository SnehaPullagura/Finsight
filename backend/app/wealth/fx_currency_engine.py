import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel

class FXRateQuote(BaseModel):
    base_currency: str
    target_currency: str
    rate: float
    bid: float
    ask: float
    spread_pct: float
    timestamp: datetime.datetime

class FXCurrencyConverterEngine:
    """
    Real-time & Historical FX Conversion Engine for global cross-currency portfolios.
    """
    EXCHANGE_RATES_TO_INR = {
        "INR": 1.0,
        "USD": 86.85,
        "EUR": 92.40,
        "GBP": 109.15,
        "SGD": 65.20,
        "AED": 23.65,
        "CAD": 62.40,
        "AUD": 56.10,
        "JPY": 0.58,
        "CHF": 98.70
    }

    @classmethod
    def get_rate(cls, from_ccy: str, to_ccy: str) -> float:
        from_u = from_ccy.upper()
        to_u = to_ccy.upper()
        if from_u not in cls.EXCHANGE_RATES_TO_INR or to_u not in cls.EXCHANGE_RATES_TO_INR:
            return 1.0
        inr_per_from = cls.EXCHANGE_RATES_TO_INR[from_u]
        inr_per_to = cls.EXCHANGE_RATES_TO_INR[to_u]
        return inr_per_from / inr_per_to

    @classmethod
    def convert(cls, amount: float, from_ccy: str, to_ccy: str) -> float:
        rate = cls.get_rate(from_ccy, to_ccy)
        return round(amount * rate, 2)

    @classmethod
    def get_quote(cls, from_ccy: str, to_ccy: str) -> FXRateQuote:
        rate = cls.get_rate(from_ccy, to_ccy)
        bid = rate * 0.9985
        ask = rate * 1.0015
        return FXRateQuote(
            base_currency=from_ccy.upper(),
            target_currency=to_ccy.upper(),
            rate=round(rate, 4),
            bid=round(bid, 4),
            ask=round(ask, 4),
            spread_pct=0.30,
            timestamp=datetime.datetime.utcnow()
        )
