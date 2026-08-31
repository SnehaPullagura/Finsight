from typing import Any, Dict, List, Optional

class TotalAddressableMarketModeler:
    @staticmethod
    def calculate_tam_sam_som(
        total_global_target_accounts: int,
        servicable_accounts_pct: float,
        obtainable_market_pct: float,
        average_annual_contract_value: float
    ) -> Dict[str, Any]:
        tam_accounts = total_global_target_accounts
        sam_accounts = int(tam_accounts * (servicable_accounts_pct / 100.0))
        som_accounts = int(sam_accounts * (obtainable_market_pct / 100.0))

        tam_value = round(tam_accounts * average_annual_contract_value, 2)
        sam_value = round(sam_accounts * average_annual_contract_value, 2)
        som_value = round(som_accounts * average_annual_contract_value, 2)

        return {
            "total_addressable_market_accounts": tam_accounts,
            "total_addressable_market_value": tam_value,
            "serviceable_addressable_market_accounts": sam_accounts,
            "serviceable_addressable_market_value": sam_value,
            "serviceable_obtainable_market_accounts": som_accounts,
            "serviceable_obtainable_market_value": som_value,
            "average_acv": average_annual_contract_value
        }
