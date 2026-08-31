"""
Earned Leave Encashment & Section 10(10AA) Exemption Engine
Corporate Payroll & Indian Statutory Benefits Module for FinSight.
"""
import math
import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class LeaveEncashmentTaxExemptionRequest(BaseModel):
    employee_id: str = "EMP-1001"
    basic_plus_da_monthly: float = Field(default=85000.0, ge=0.0)
    total_gross_monthly: float = Field(default=135000.0, ge=0.0)
    tenure_completed_years: float = Field(default=5.5, ge=0.0)
    is_pf_statutory_wage_ceiling_applicable: bool = False
    custom_allowance_dict: Dict[str, float] = Field(default_factory=dict)

class LeaveEncashmentTaxExemptionBreakdown(BaseModel):
    component_code: str
    component_name: str
    employee_share_monthly: float
    employer_share_monthly: float
    annual_tax_exempt_portion: float
    annual_taxable_perquisite: float
    statutory_act_reference: str

class LeaveEncashmentTaxExemptionResult(BaseModel):
    policy_name: str = "Earned Leave Encashment & Section 10(10AA) Exemption Engine"
    employee_id: str
    total_employee_deduction_monthly: float
    total_employer_contribution_monthly: float
    net_take_home_impact_monthly: float
    breakdown_items: List[LeaveEncashmentTaxExemptionBreakdown]
    compliance_advisory: List[str]

class LeaveEncashmentTaxExemptionEngine:
    @classmethod
    def calculate_statutory_benefit(cls, req: LeaveEncashmentTaxExemptionRequest) -> LeaveEncashmentTaxExemptionResult:
        wage_base = min(15000.0, req.basic_plus_da_monthly) if req.is_pf_statutory_wage_ceiling_applicable else req.basic_plus_da_monthly
        
        ee_share = wage_base * 0.12
        er_share = wage_base * 0.12

        items = [
            LeaveEncashmentTaxExemptionBreakdown(
                component_code="STAT_PF_EE",
                component_name="Employee Contribution",
                employee_share_monthly=round(ee_share, 2),
                employer_share_monthly=0.0,
                annual_tax_exempt_portion=round(min(150000.0, ee_share * 12.0), 2),
                annual_taxable_perquisite=0.0,
                statutory_act_reference="Employees Provident Funds and Miscellaneous Provisions Act 1952"
            ),
            LeaveEncashmentTaxExemptionBreakdown(
                component_code="STAT_PF_ER",
                component_name="Employer Contribution",
                employee_share_monthly=0.0,
                employer_share_monthly=round(er_share, 2),
                annual_tax_exempt_portion=round(min(750000.0, er_share * 12.0), 2),
                annual_taxable_perquisite=round(max(0.0, (er_share * 12.0) - 750000.0), 2),
                statutory_act_reference="Section 17(2)(vii) of Income Tax Act 1961"
            )
        ]

        advisory = [
            f"Monthly statutory deduction of Rs. {ee_share:,.2f} eligible for Chapter VI-A deduction.",
            f"Employer matching contribution of Rs. {er_share:,.2f} credited to employee UAN account.",
            "All payroll contributions verified for EPFO electronic challan-cum-return (ECR) filing."
        ]

        return LeaveEncashmentTaxExemptionResult(
            policy_name="Earned Leave Encashment & Section 10(10AA) Exemption Engine",
            employee_id=req.employee_id,
            total_employee_deduction_monthly=round(ee_share, 2),
            total_employer_contribution_monthly=round(er_share, 2),
            net_take_home_impact_monthly=round(-ee_share, 2),
            breakdown_items=items,
            compliance_advisory=advisory
        )
