import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel

class TaxDeductions80C(BaseModel):
    epf_employee_contribution: float = 0.0
    ppf_deposit: float = 0.0
    elss_mutual_funds: float = 0.0
    life_insurance_premium: float = 0.0
    home_loan_principal: float = 0.0
    tuition_fees_children: float = 0.0
    sukanya_samriddhi: float = 0.0

class TaxDeductionsOther(BaseModel):
    nps_80ccd_1b: float = 0.0 # Up to Rs. 50,000 additional
    health_insurance_80d_self: float = 0.0 # Up to Rs. 25,000
    health_insurance_80d_parents: float = 0.0 # Up to Rs. 50,000 (senior)
    education_loan_interest_80e: float = 0.0 # Full interest deductible
    home_loan_interest_24b: float = 0.0 # Up to Rs. 2,00,000 for self-occupied
    savings_interest_80tta: float = 0.0 # Up to Rs. 10,000

class HRAExemptionInputs(BaseModel):
    basic_salary_annual: float
    dearness_allowance_annual: float = 0.0
    hra_received_annual: float
    rent_paid_annual: float
    is_metro_city: bool = True # 50% for Delhi/Mumbai/Kolkata/Chennai, 40% for others

class IncomeTaxCalculationResult(BaseModel):
    financial_year: str = "FY 2026-27 (AY 2027-28)"
    gross_total_income: float
    
    # Old Regime Breakdown
    old_regime_standard_deduction: float
    old_regime_hra_exemption: float
    old_regime_total_deductions_80c: float
    old_regime_total_other_deductions: float
    old_regime_net_taxable_income: float
    old_regime_tax_payable: float
    old_regime_cess_4pct: float
    old_regime_total_liability: float

    # New Regime Breakdown (Section 115BAC)
    new_regime_standard_deduction: float
    new_regime_net_taxable_income: float
    new_regime_tax_payable: float
    new_regime_section_87a_rebate: float
    new_regime_cess_4pct: float
    new_regime_total_liability: float

    # Recommendation
    recommended_regime: str
    tax_savings_with_recommended: float
    tax_optimization_tips: List[str]

class IndianIncomeTaxEngine:
    """
    Comprehensive Income Tax Calculation Engine for Individual Salaried & Professional Taxpayers.
    Implements FY 2026-27 tax slabs for both Old and New Tax Regimes (u/s 115BAC).
    """
    @staticmethod
    def calculate_hra_exemption(inputs: HRAExemptionInputs) -> float:
        salary = inputs.basic_salary_annual + inputs.dearness_allowance_annual
        if salary <= 0 or inputs.rent_paid_annual <= 0:
            return 0.0
        
        # Rule 2A formula: Minimum of 3 criteria
        c1 = inputs.hra_received_annual
        c2 = max(0.0, inputs.rent_paid_annual - (0.10 * salary))
        c3 = (0.50 * salary) if inputs.is_metro_city else (0.40 * salary)
        
        return min(c1, c2, c3)

    @classmethod
    def compute_tax(
        cls,
        gross_salary: float,
        other_incomes: float = 0.0,
        hra_inputs: Optional[HRAExemptionInputs] = None,
        deductions_80c: Optional[TaxDeductions80C] = None,
        deductions_other: Optional[TaxDeductionsOther] = None
    ) -> IncomeTaxCalculationResult:
        gross_total = gross_salary + other_incomes
        
        # 1. OLD REGIME COMPUTATION
        old_std_deduction = 50000.0 if gross_salary > 0 else 0.0
        hra_exempt = cls.calculate_hra_exemption(hra_inputs) if hra_inputs else 0.0
        
        # 80C Capped at 1.5 Lakhs
        raw_80c = 0.0
        if deductions_80c:
            raw_80c = sum([
                deductions_80c.epf_employee_contribution,
                deductions_80c.ppf_deposit,
                deductions_80c.elss_mutual_funds,
                deductions_80c.life_insurance_premium,
                deductions_80c.home_loan_principal,
                deductions_80c.tuition_fees_children,
                deductions_80c.sukanya_samriddhi
            ])
        capped_80c = min(150000.0, raw_80c)

        # Other Deductions
        other_ded_total = 0.0
        if deductions_other:
            nps = min(50000.0, deductions_other.nps_80ccd_1b)
            health_self = min(25000.0, deductions_other.health_insurance_80d_self)
            health_parents = min(50000.0, deductions_other.health_insurance_80d_parents)
            home_loan_int = min(200000.0, deductions_other.home_loan_interest_24b)
            tta = min(10000.0, deductions_other.savings_interest_80tta)
            edu_loan = deductions_other.education_loan_interest_80e
            other_ded_total = nps + health_self + health_parents + home_loan_int + tta + edu_loan

        old_net_taxable = max(0.0, gross_total - old_std_deduction - hra_exempt - capped_80c - other_ded_total)
        
        # Old Regime Slabs:
        # 0 - 2.5L: Nil
        # 2.5L - 5.0L: 5%
        # 5.0L - 10.0L: 20%
        # > 10.0L: 30%
        old_tax = 0.0
        if old_net_taxable > 1000000:
            old_tax += (old_net_taxable - 1000000) * 0.30 + 100000.0 + 12500.0
        elif old_net_taxable > 500000:
            old_tax += (old_net_taxable - 500000) * 0.20 + 12500.0
        elif old_net_taxable > 250000:
            old_tax += (old_net_taxable - 250000) * 0.05

        # Section 87A rebate under Old Regime (up to 5L taxable income)
        if old_net_taxable <= 500000:
            old_tax = 0.0

        old_cess = old_tax * 0.04
        old_total = old_tax + old_cess

        # 2. NEW REGIME COMPUTATION (Section 115BAC - Default Regime)
        # Standard deduction in New Regime: Rs. 75,000 for salaried
        new_std_deduction = 75000.0 if gross_salary > 0 else 0.0
        new_net_taxable = max(0.0, gross_total - new_std_deduction)

        # Slabs for FY 2026-27 (New Regime):
        # 0 - 3,00,000: Nil
        # 3,00,001 - 7,00,000: 5%
        # 7,00,001 - 10,00,000: 10%
        # 10,00,001 - 12,00,000: 15%
        # 12,00,001 - 15,00,000: 20%
        # Above 15,00,000: 30%
        new_tax = 0.0
        rem = new_net_taxable
        if rem > 1500000:
            new_tax += (rem - 1500000) * 0.30
            rem = 1500000
        if rem > 1200000:
            new_tax += (rem - 1200000) * 0.20
            rem = 1200000
        if rem > 1000000:
            new_tax += (rem - 1000000) * 0.15
            rem = 1000000
        if rem > 700000:
            new_tax += (rem - 700000) * 0.10
            rem = 700000
        if rem > 300000:
            new_tax += (rem - 300000) * 0.05

        # Section 87A rebate under New Regime (up to 7 Lakhs taxable income)
        rebate_87a = 0.0
        if new_net_taxable <= 700000:
            rebate_87a = new_tax
            new_tax = 0.0

        new_cess = new_tax * 0.04
        new_total = new_tax + new_cess

        # Comparison & Recommendation
        rec = "New Tax Regime (Section 115BAC)" if new_total <= old_total else "Old Tax Regime"
        savings = abs(old_total - new_total)

        tips = []
        if rec == "New Tax Regime (Section 115BAC)":
            tips.append("New Regime is more beneficial by Rs. {:,.2f} without needing locked investments.".format(savings))
        else:
            tips.append("Old Regime saves Rs. {:,.2f} due to high HRA and Chapter VI-A deductions.".format(savings))
        if capped_80c < 150000.0:
            tips.append("You have an unutilized 80C room of Rs. {:,.2f} via ELSS mutual funds or PPF.".format(150000.0 - capped_80c))

        return IncomeTaxCalculationResult(
            gross_total_income=gross_total,
            old_regime_standard_deduction=old_std_deduction,
            old_regime_hra_exemption=hra_exempt,
            old_regime_total_deductions_80c=capped_80c,
            old_regime_total_other_deductions=other_ded_total,
            old_regime_net_taxable_income=old_net_taxable,
            old_regime_tax_payable=old_tax,
            old_regime_cess_4pct=old_cess,
            old_regime_total_liability=old_total,
            new_regime_standard_deduction=new_std_deduction,
            new_regime_net_taxable_income=new_net_taxable,
            new_regime_tax_payable=new_tax,
            new_regime_section_87a_rebate=rebate_87a,
            new_regime_cess_4pct=new_cess,
            new_regime_total_liability=new_total,
            recommended_regime=rec,
            tax_savings_with_recommended=savings,
            tax_optimization_tips=tips
        )
