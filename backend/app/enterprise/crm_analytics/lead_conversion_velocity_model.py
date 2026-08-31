from datetime import date
from typing import Any, Dict, List, Optional

class LeadConversionVelocityModel:
    @staticmethod
    def calculate_sales_cycle_velocity(
        qualified_leads: int,
        win_rate_pct: float,
        average_deal_size: float,
        sales_cycle_days: float
    ) -> Dict[str, Any]:
        win_rate_decimal = win_rate_pct / 100.0
        cycle_days = max(1.0, sales_cycle_days)
        
        # Pipeline Velocity Formula: V = (Leads * WinRate * DealSize) / CycleLengthDays
        daily_velocity = (qualified_leads * win_rate_decimal * average_deal_size) / cycle_days
        monthly_velocity = daily_velocity * 30.0
        annual_velocity = daily_velocity * 365.0

        return {
            "qualified_leads_count": qualified_leads,
            "win_rate_percentage": win_rate_pct,
            "average_deal_size": average_deal_size,
            "sales_cycle_length_days": sales_cycle_days,
            "daily_revenue_velocity": round(daily_velocity, 2),
            "monthly_projected_velocity": round(monthly_velocity, 2),
            "annual_projected_velocity": round(annual_velocity, 2)
        }
