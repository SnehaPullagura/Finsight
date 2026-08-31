import math
from typing import Dict, List, Optional, Tuple
from decimal import Decimal, ROUND_HALF_UP

CURRENCY_EXCHANGE_RATES: Dict[str, float] = {
    "USD": 1.0,
    "EUR": 0.92,
    "GBP": 0.79,
    "CAD": 1.36,
    "AUD": 1.52,
    "JPY": 155.20,
    "INR": 83.45,
    "SGD": 1.35,
    "CHF": 0.91,
}

class CurrencyConversionService:
    @staticmethod
    def convert(amount: float, from_currency: str, to_currency: str) -> float:
        from_curr = from_currency.upper()
        to_curr = to_currency.upper()
        if from_curr == to_curr:
            return round(amount, 2)

        base_usd_rate = CURRENCY_EXCHANGE_RATES.get(from_curr, 1.0)
        target_rate = CURRENCY_EXCHANGE_RATES.get(to_curr, 1.0)

        # Convert to USD base then to target
        amount_usd = amount / base_usd_rate
        converted = amount_usd * target_rate
        return round(converted, 2)

    @staticmethod
    def get_supported_currencies() -> List[str]:
        return list(CURRENCY_EXCHANGE_RATES.keys())

class CPQPricingEngine:
    @staticmethod
    def evaluate_volume_tier(quantity: int, tiers: list) -> Tuple[float, float]:
        selected_discount_pct = 0.0
        selected_flat_amount = 0.0

        for tier in sorted(tiers, key=lambda t: t.tier_order):
            lower = tier.lower_bound
            upper = tier.upper_bound or float("inf")

            if lower <= quantity <= upper:
                selected_discount_pct = float(tier.discount_percentage)
                selected_flat_amount = float(tier.flat_discount_amount or 0.0)
                break

        return selected_discount_pct, selected_flat_amount

    @staticmethod
    def calculate_line_item(
        unit_price: float,
        quantity: int,
        discount_percentage: float = 0.0,
        flat_discount: float = 0.0,
        tax_rate_pct: float = 0.0
    ) -> Dict[str, float]:
        subtotal = round(unit_price * quantity, 2)
        pct_discount_amount = round(subtotal * (discount_percentage / 100.0), 2)
        total_discount = min(subtotal, round(pct_discount_amount + flat_discount, 2))
        
        net_amount = max(0.0, round(subtotal - total_discount, 2))
        tax_amount = round(net_amount * (tax_rate_pct / 100.0), 2)
        total_amount = round(net_amount + tax_amount, 2)

        return {
            "subtotal": subtotal,
            "discount_amount": total_discount,
            "net_amount": net_amount,
            "tax_amount": tax_amount,
            "total_amount": total_amount
        }
