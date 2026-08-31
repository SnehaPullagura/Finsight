from typing import Any, Dict, List, Optional

class CustomerChampionIdentifier:
    @staticmethod
    def identify_promoters_and_power_users(users_activity: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        champions = []
        for u in users_activity:
            email = u.get("email")
            nps = int(u.get("nps_score", 8))
            sessions = int(u.get("sessions_monthly", 20))
            is_admin = bool(u.get("is_admin", False))

            if nps >= 9 and sessions >= 25:
                champions.append({
                    "user_email": email,
                    "account_name": u.get("account_name"),
                    "nps_rating": nps,
                    "monthly_sessions": sessions,
                    "is_account_admin": is_admin,
                    "champion_role": "Executive Sponsor" if is_admin else "Product Power Champion",
                    "advocacy_readiness": "Ready for Case Study & Expansion Co-Pitch"
                })

        return champions
