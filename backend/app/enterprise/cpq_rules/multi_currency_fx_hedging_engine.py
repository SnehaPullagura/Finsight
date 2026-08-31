from typing import Any, Dict, List, Optional

class MultiCurrencyFXHedgingEngine:
    """
    Multi-Currency CPQ Pricing & FX Volatility Buffer:
    Converts USD base quotes to EUR, GBP, JPY, AUD, CAD with automated 2.5% FX risk buffer.
    """
    FX_SPOT_RATES = {
        "EUR": 0.92,
        "GBP": 0.78,
        "JPY": 155.40,
        "AUD": 1.52,
        "CAD": 1.36,
        "USD": 1.00
    }

    @classmethod
    def convert_and_hedge_quote(
        cls,
        usd_amount: float,
        target_currency: str,
        contract_term_years: int = 1
    ) -> Dict[str, Any]:
        curr = target_currency.upper()
        rate = cls.FX_SPOT_RATES.get(curr, 1.0)
        spot_converted = usd_amount * rate

        # FX volatility buffer (2.5% per term year)
        fx_buffer_pct = 2.5 * contract_term_years
        hedged_total = round(spot_converted * (1.0 + (fx_buffer_pct / 100.0)), 2)

        return {
            "base_usd_amount": usd_amount,
            "target_currency": curr,
            "spot_exchange_rate": rate,
            "spot_converted_amount": round(spot_converted, 2),
            "term_years": contract_term_years,
            "fx_volatility_buffer_pct": fx_buffer_pct,
            "final_hedged_local_currency_quote": hedged_total,
            "currency_symbol": "€" if curr == "EUR" else "£" if curr == "GBP" else "¥" if curr == "JPY" else "$"
        }
