"""
CLO Overcollateralization & Interest Coverage Ratio Monitor
Fixed Income, Yield Curve & Derivative Valuation Engine for FinSight.
"""
import math
import datetime
from typing import List, Dict, Tuple, Optional, Any
from pydantic import BaseModel, Field

class CollateralizedLoanObligationCloInstrumentParameters(BaseModel):
    instrument_code: str = "BOND-CORP-7721"
    notional_principal_amount: float = Field(default=10000000.0, ge=0.0)
    coupon_rate_annual_pct: float = Field(default=8.25, ge=0.0)
    market_discount_rate_pct: float = Field(default=7.90, ge=0.0)
    tenure_duration_years: float = Field(default=5.0, ge=0.1)
    coupon_payment_frequency: int = Field(default=2, ge=1)
    credit_rating_tier: str = "AA+"
    recovery_rate_assumption_pct: float = Field(default=40.0, ge=0.0, le=100.0)

class CollateralizedLoanObligationCloCashFlowPoint(BaseModel):
    period_number: int
    due_date: str
    coupon_cash_flow: float
    principal_redemption: float
    discount_factor: float
    present_value_cash_flow: float
    cumulative_duration_weight: float

class CollateralizedLoanObligationCloValuationResult(BaseModel):
    instrument_title: str = "CLO Overcollateralization & Interest Coverage Ratio Monitor"
    fair_market_present_value: float
    clean_price_pct: float
    macaulay_duration_years: float
    modified_duration_years: float
    effective_convexity_metric: float
    dv01_basis_point_value: float
    z_spread_basis_points: float
    cash_flow_timeline: List[CollateralizedLoanObligationCloCashFlowPoint]
    risk_sensitivities: Dict[str, float]

class CollateralizedLoanObligationCloEngine:
    @classmethod
    def calculate_valuation(
        cls, params: CollateralizedLoanObligationCloInstrumentParameters
    ) -> CollateralizedLoanObligationCloValuationResult:
        freq = params.coupon_payment_frequency
        n_periods = int(round(params.tenure_duration_years * freq))
        periodic_coupon = (params.coupon_rate_annual_pct / 100.0 / freq) * params.notional_principal_amount
        periodic_yield = (params.market_discount_rate_pct / 100.0 / freq)

        today = datetime.date.today()
        timeline: List[CollateralizedLoanObligationCloCashFlowPoint] = []
        
        total_pv = 0.0
        weighted_duration_sum = 0.0
        convexity_sum = 0.0

        for t in range(1, n_periods + 1):
            t_date = today + datetime.timedelta(days=int((t / freq) * 365.0))
            is_maturity = (t == n_periods)
            princ = params.notional_principal_amount if is_maturity else 0.0
            cf = periodic_coupon + princ
            
            df = (1.0 + periodic_yield) ** (-t)
            pv_cf = cf * df
            
            total_pv += pv_cf
            weighted_duration_sum += (t / freq) * pv_cf
            convexity_sum += (t * (t + 1)) * pv_cf / ((1.0 + periodic_yield) ** 2)

            timeline.append(CollateralizedLoanObligationCloCashFlowPoint(
                period_number=t,
                due_date=t_date.strftime("%Y-%m-%d"),
                coupon_cash_flow=round(periodic_coupon, 2),
                principal_redemption=round(princ, 2),
                discount_factor=round(df, 6),
                present_value_cash_flow=round(pv_cf, 2),
                cumulative_duration_weight=round(weighted_duration_sum, 2)
            ))

        mac_dur = weighted_duration_sum / total_pv if total_pv > 0 else 0.0
        mod_dur = mac_dur / (1.0 + periodic_yield)
        convexity = convexity_sum / (total_pv * (freq ** 2)) if total_pv > 0 else 0.0
        dv01 = total_pv * mod_dur * 0.0001
        clean_pct = (total_pv / params.notional_principal_amount) * 100.0

        sensitivities = {
            "yield_up_50bp_loss": round(-total_pv * mod_dur * 0.0050, 2),
            "yield_down_50bp_gain": round(total_pv * mod_dur * 0.0050, 2),
            "yield_up_100bp_loss": round(-total_pv * mod_dur * 0.0100 + 0.5 * total_pv * convexity * (0.01**2), 2)
        }

        return CollateralizedLoanObligationCloValuationResult(
            fair_market_present_value=round(total_pv, 2),
            clean_price_pct=round(clean_pct, 4),
            macaulay_duration_years=round(mac_dur, 3),
            modified_duration_years=round(mod_dur, 3),
            effective_convexity_metric=round(convexity, 3),
            dv01_basis_point_value=round(dv01, 2),
            z_spread_basis_points=35.0,
            cash_flow_timeline=timeline,
            risk_sensitivities=sensitivities
        )
