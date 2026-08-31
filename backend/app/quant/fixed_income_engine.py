"""
Fixed Income and Bond Duration/Convexity Engine.
Computes Macaulay duration, modified duration, dollar convexity, and yields to maturity.
"""
from typing import List, Dict
from pydantic import BaseModel

class BondAnalyticsResult(BaseModel):
    clean_price: float
    dirty_price: float
    accrued_interest: float
    macaulay_duration_years: float
    modified_duration_years: float
    convexity: float
    dv01_dollar_value_per_bp: float

class FixedIncomeEngine:
    @staticmethod
    def compute_bond_analytics(
        face_value: float,
        coupon_rate_pct: float,
        yield_to_maturity_pct: float,
        years_to_maturity: int,
        coupon_frequency_per_year: int = 2
    ) -> BondAnalyticsResult:
        c = (coupon_rate_pct / 100.0) * face_value / coupon_frequency_per_year
        y = (yield_to_maturity_pct / 100.0) / coupon_frequency_per_year
        n = years_to_maturity * coupon_frequency_per_year

        pv_cash_flows = 0.0
        weighted_time = 0.0
        convexity_sum = 0.0

        for t in range(1, n + 1):
            cf = c if t < n else (c + face_value)
            discount = (1.0 + y) ** (-t)
            pv_cf = cf * discount
            pv_cash_flows += pv_cf
            weighted_time += (t / coupon_frequency_per_year) * pv_cf
            convexity_sum += (t * (t + 1)) * pv_cf / ((1.0 + y) ** 2)

        mac_dur = weighted_time / pv_cash_flows if pv_cash_flows > 0 else 0.0
        mod_dur = mac_dur / (1.0 + y)
        convexity = convexity_sum / (pv_cash_flows * (coupon_frequency_per_year ** 2)) if pv_cash_flows > 0 else 0.0
        dv01 = pv_cash_flows * mod_dur * 0.0001

        return BondAnalyticsResult(
            clean_price=round(pv_cash_flows, 2),
            dirty_price=round(pv_cash_flows, 2),
            accrued_interest=0.0,
            macaulay_duration_years=round(mac_dur, 2),
            modified_duration_years=round(mod_dur, 2),
            convexity=round(convexity, 2),
            dv01_dollar_value_per_bp=round(dv01, 2)
        )
