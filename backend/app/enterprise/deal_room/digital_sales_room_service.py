from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class DigitalSalesRoomService:
    """
    Enterprise Digital Sales Room (DSR) & Buyer Experience Portal:
    Creates personalized executive deal microsites for buyer stakeholders,
    curating case studies, proposals, security whitepapers, and mutual action plans.
    """
    @staticmethod
    def create_sales_room(
        deal_id: str,
        account_name: str,
        champion_email: str,
        economic_buyer_email: str,
        curated_documents: List[Dict[str, Any]],
        expiry_days: int = 60
    ) -> Dict[str, Any]:
        room_id = f"dsr_{deal_id}_{int(datetime.now(timezone.utc).timestamp())}"
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(days=expiry_days)

        return {
            "sales_room_id": room_id,
            "deal_id": deal_id,
            "account_name": account_name,
            "portal_url": f"https://dealroom.clientflow.io/room/{room_id}",
            "champion_email": champion_email,
            "economic_buyer_email": economic_buyer_email,
            "curated_documents_count": len(curated_documents),
            "documents": curated_documents,
            "created_at": now.isoformat(),
            "expires_at": expires_at.isoformat(),
            "nda_signature_required": True,
            "is_password_protected": True,
            "room_status": "ACTIVE_PUBLISHED"
        }

    @staticmethod
    def record_buyer_session(
        room_id: str,
        visitor_email: str,
        time_spent_seconds: int,
        documents_viewed: List[str]
    ) -> Dict[str, Any]:
        return {
            "session_id": f"sess_{int(datetime.now(timezone.utc).timestamp() * 1000)}",
            "sales_room_id": room_id,
            "visitor_email": visitor_email,
            "duration_seconds": time_spent_seconds,
            "documents_viewed": documents_viewed,
            "is_high_intent_session": time_spent_seconds >= 300 or len(documents_viewed) >= 3,
            "recorded_at": datetime.now(timezone.utc).isoformat()
        }
