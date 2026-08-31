from typing import Dict, List, Optional

class MultiCurrencyExchangeMatrix:
    RATES_TO_USD = {
        "USD": 1.0,
        "EUR": 1.087,
        "GBP": 1.265,
        "CAD": 0.735,
        "AUD": 0.658,
        "JPY": 0.00644,
        "INR": 0.0120,
        "SGD": 0.741,
        "CHF": 1.10
    }

    @staticmethod
    def convert_amount(amount: float, source_currency: str, target_currency: str) -> float:
        src = source_currency.upper()
        dst = target_currency.upper()
        if src == dst:
            return round(amount, 2)

        usd_val = amount * MultiCurrencyExchangeMatrix.RATES_TO_USD.get(src, 1.0)
        target_rate = MultiCurrencyExchangeMatrix.RATES_TO_USD.get(dst, 1.0)
        final_val = usd_val / target_rate
        return round(final_val, 2)
