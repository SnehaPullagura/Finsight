import math
from typing import Dict, List, Optional
from pydantic import BaseModel

class BuyVsRentInputs(BaseModel):
    property_purchase_price: float = 12000000.0 # 1.2 Crore
    down_payment_pct: float = 20.0
    loan_interest_rate_pct: float = 8.5
    loan_tenure_years: int = 20
    property_registration_and_stamp_duty_pct: float = 6.5
    annual_maintenance_and_property_tax_pct: float = 1.0
    expected_property_appreciation_pct: float = 5.5
    
    # Renting parameters
    initial_monthly_rent: float = 35000.0
    annual_rent_increase_pct: float = 7.0
    investment_return_on_saved_capital_pct: float = 12.0 # Nifty 50 Equity SIP return

class BuyVsRentYearlyComparison(BaseModel):
    year: int
    buyer_equity_wealth: float
    renter_investment_wealth: float
    net_wealth_difference_buyer_minus_renter: float
    cumulative_rent_paid: float
    cumulative_emi_paid: float

class BuyVsRentResult(BaseModel):
    verdict: str # BUY_RECOMMENDED or RENT_AND_INVEST_RECOMMENDED
    summary_explanation: str
    breakeven_year: Optional[int]
    buyer_net_worth_at_20yr: float
    renter_net_worth_at_20yr: float
    total_buyer_cash_outlay: float
    total_renter_cash_outlay: float
    monthly_emi_amount: float
    yearly_breakdown: List[BuyVsRentYearlyComparison]

class RealEstateBuyVsRentSimulator:
    """
    Institutional Buy vs Rent Financial Simulator.
    Compares total cost of ownership (EMIs, stamp duty, maintenance, property taxes)
    against opportunity cost of capital invested in equity index funds.
    """
    @classmethod
    def simulate(cls, inp: BuyVsRentInputs) -> BuyVsRentResult:
        down_payment = inp.property_purchase_price * (inp.down_payment_pct / 100.0)
        upfront_costs = down_payment + (inp.property_purchase_price * (inp.property_registration_and_stamp_duty_pct / 100.0))
        loan_principal = inp.property_purchase_price - down_payment
        
        # Monthly EMI calculation
        r_mo = inp.loan_interest_rate_pct / 100.0 / 12.0
        n_mo = inp.loan_tenure_years * 12
        if r_mo > 0:
            emi = (loan_principal * r_mo * ((1.0 + r_mo) ** n_mo)) / (((1.0 + r_mo) ** n_mo) - 1.0)
        else:
            emi = loan_principal / n_mo

        annual_emi = emi * 12.0

        # Simulation states
        prop_val = inp.property_purchase_price
        loan_rem = loan_principal
        renter_portfolio = upfront_costs # Renter invests the down payment + stamp duty
        
        cum_emi = 0.0
        cum_rent = 0.0
        curr_rent_mo = inp.initial_monthly_rent
        breakeven = None
        yearly: List[BuyVsRentYearlyComparison] = []

        for yr in range(1, inp.loan_tenure_years + 1):
            # 1. Buyer side
            prop_val *= (1.0 + (inp.expected_property_appreciation_pct / 100.0))
            maint = prop_val * (inp.annual_maintenance_and_property_tax_pct / 100.0)
            
            # Amortize loan for 12 months
            for _ in range(12):
                if loan_rem > 0:
                    int_mo = loan_rem * r_mo
                    princ_mo = emi - int_mo
                    loan_rem = max(0.0, loan_rem - princ_mo)
            
            buyer_equity = prop_val - loan_rem
            buyer_annual_cash = annual_emi + maint
            cum_emi += annual_emi

            # 2. Renter side
            annual_rent = curr_rent_mo * 12.0
            cum_rent += annual_rent
            
            # Cash flow difference saved by renter (Buyer outlay - Renter rent)
            renter_savings = max(0.0, buyer_annual_cash - annual_rent)
            
            # Renter portfolio compounds
            renter_portfolio = renter_portfolio * (1.0 + (inp.investment_return_on_saved_capital_pct / 100.0)) + renter_savings
            curr_rent_mo *= (1.0 + (inp.annual_rent_increase_pct / 100.0))

            wealth_diff = buyer_equity - renter_portfolio
            if breakeven is None and wealth_diff > 0:
                breakeven = yr

            yearly.append(BuyVsRentYearlyComparison(
                year=yr,
                buyer_equity_wealth=round(buyer_equity, 2),
                renter_investment_wealth=round(renter_portfolio, 2),
                net_wealth_difference_buyer_minus_renter=round(wealth_diff, 2),
                cumulative_rent_paid=round(cum_rent, 2),
                cumulative_emi_paid=round(cum_emi, 2)
            ))

        final_buyer_nw = yearly[-1].buyer_equity_wealth
        final_renter_nw = yearly[-1].renter_investment_wealth
        verdict = "BUY_RECOMMENDED" if final_buyer_nw >= final_renter_nw else "RENT_AND_INVEST_RECOMMENDED"

        summary = (
            f"Over {inp.loan_tenure_years} years, {'Buying' if verdict == 'BUY_RECOMMENDED' else 'Renting & Investing'} "
            f"yields a net wealth advantage of Rs. {abs(final_buyer_nw - final_renter_nw):,.2f}."
        )

        return BuyVsRentResult(
            verdict=verdict,
            summary_explanation=summary,
            breakeven_year=breakeven,
            buyer_net_worth_at_20yr=round(final_buyer_nw, 2),
            renter_net_worth_at_20yr=round(final_renter_nw, 2),
            total_buyer_cash_outlay=round(cum_emi + upfront_costs, 2),
            total_renter_cash_outlay=round(cum_rent, 2),
            monthly_emi_amount=round(emi, 2),
            yearly_breakdown=yearly
        )
