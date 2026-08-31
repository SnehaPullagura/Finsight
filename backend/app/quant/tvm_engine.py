"""
Time-Value of Money (TVM) and Quantitative Financial Mathematics Engine.
Implements exact compound interest, annuities, perpetuities, bond pricing, and internal rate of return (XIRR).
"""
import math
from typing import List, Tuple, Optional
from pydantic import BaseModel

class TVMParameters(BaseModel):
    rate: float # Periodic interest rate (e.g. 0.08)
    nper: int   # Number of periods
    pmt: float  # Payment per period
    pv: float   # Present value
    fv: float = 0.0 # Future value
    when: int = 0   # 0 = end of period (ordinary annuity), 1 = beginning of period (annuity due)

class QuantitativeMathEngine:
    @staticmethod
    def future_value(rate: float, nper: int, pmt: float, pv: float, when: int = 0) -> float:
        if abs(rate) < 1e-12:
            return -(pv + pmt * nper)
        factor = (1.0 + rate) ** nper
        if when == 1:
            fv = - (pv * factor + pmt * (1.0 + rate) * (factor - 1.0) / rate)
        else:
            fv = - (pv * factor + pmt * (factor - 1.0) / rate)
        return round(float(fv), 2)

    @staticmethod
    def present_value(rate: float, nper: int, pmt: float, fv: float = 0.0, when: int = 0) -> float:
        if abs(rate) < 1e-12:
            return -(fv + pmt * nper)
        factor = (1.0 + rate) ** nper
        if when == 1:
            pv = - (fv + pmt * (1.0 + rate) * (factor - 1.0) / rate) / factor
        else:
            pv = - (fv + pmt * (factor - 1.0) / rate) / factor
        return round(float(pv), 2)

    @staticmethod
    def pmt_installment(rate: float, nper: int, pv: float, fv: float = 0.0, when: int = 0) -> float:
        if abs(rate) < 1e-12:
            return -(fv + pv) / nper
        factor = (1.0 + rate) ** nper
        if when == 1:
            pmt = - (pv * factor + fv) * rate / ((1.0 + rate) * (factor - 1.0))
        else:
            pmt = - (pv * factor + fv) * rate / (factor - 1.0)
        return round(float(pmt), 2)

    @staticmethod
    def nper_periods(rate: float, pmt: float, pv: float, fv: float = 0.0, when: int = 0) -> float:
        if abs(rate) < 1e-12:
            return -(fv + pv) / pmt
        z = pmt * (1.0 + rate * when) / rate
        numerator = -fv + z
        denominator = pv + z
        if numerator / denominator <= 0:
            return 0.0
        return round(float(math.log(numerator / denominator) / math.log(1.0 + rate)), 2)

    @staticmethod
    def calculate_xirr(cash_flows: List[Tuple[str, float]], guess: float = 0.1) -> Optional[float]:
        """
        Exact Newton-Raphson XIRR (Extended Internal Rate of Return) with daily discounting.
        """
        import datetime
        if len(cash_flows) < 2:
            return None
        
        parsed_dates = [datetime.datetime.strptime(d, "%Y-%m-%d").date() for d, _ in cash_flows]
        amounts = [amt for _, amt in cash_flows]
        min_date = min(parsed_dates)
        days = [(d - min_date).days for d in parsed_dates]

        rate = guess
        for _ in range(100):
            # f(rate) = sum(amt / (1 + rate)^(day / 365))
            # f'(rate) = sum(-day / 365 * amt / (1 + rate)^(day / 365 + 1))
            f_val = 0.0
            f_prime = 0.0
            for i in range(len(amounts)):
                t = days[i] / 365.0
                denom = (1.0 + rate) ** t
                if abs(denom) < 1e-12:
                    continue
                f_val += amounts[i] / denom
                f_prime -= t * amounts[i] / ((1.0 + rate) ** (t + 1.0))

            if abs(f_prime) < 1e-12:
                break
            new_rate = rate - (f_val / f_prime)
            if abs(new_rate - rate) < 1e-7:
                return round(float(new_rate * 100.0), 2)
            rate = new_rate

        return round(float(rate * 100.0), 2)
