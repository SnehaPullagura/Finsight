import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/analytics/bi_engine.py
    write_file("backend/app/analytics/bi_engine.py", """import math
from datetime import datetime, date, timedelta
from typing import Any, Dict, List, Optional, Tuple

class BusinessIntelligenceEngine:
    @staticmethod
    def calculate_pipeline_velocity(
        qualified_opportunities_count: int,
        win_rate_percentage: float,
        average_deal_size: float,
        average_sales_cycle_days: float
    ) -> Dict[str, float]:
        if average_sales_cycle_days <= 0:
            return {"daily_velocity": 0.0, "monthly_velocity": 0.0, "annual_velocity": 0.0}

        win_rate_factor = win_rate_percentage / 100.0
        daily_velocity = (qualified_opportunities_count * win_rate_factor * average_deal_size) / average_sales_cycle_days
        monthly_velocity = daily_velocity * 30.0
        annual_velocity = daily_velocity * 365.0

        return {
            "daily_velocity": round(daily_velocity, 2),
            "monthly_velocity": round(monthly_velocity, 2),
            "annual_velocity": round(annual_velocity, 2),
            "inputs": {
                "opportunities": qualified_opportunities_count,
                "win_rate": win_rate_percentage,
                "avg_deal_size": average_deal_size,
                "sales_cycle_days": average_sales_cycle_days
            }
        }

    @staticmethod
    def calculate_deal_slippage(deals: List[Dict[str, Any]]) -> Dict[str, Any]:
        slipped_deals = []
        total_slipped_value = 0.0
        on_track_deals = []
        total_on_track_value = 0.0

        now = date.today()

        for d in deals:
            close_date_str = d.get("expected_close_date")
            val = float(d.get("value", 0.0))
            
            if close_date_str:
                try:
                    close_date = datetime.strptime(close_date_str, "%Y-%m-%d").date()
                except ValueError:
                    close_date = now

                if close_date < now and d.get("status") == "open":
                    slipped_deals.append(d)
                    total_slipped_value += val
                else:
                    on_track_deals.append(d)
                    total_on_track_value += val
            else:
                on_track_deals.append(d)
                total_on_track_value += val

        total_deals = len(deals)
        slippage_rate = (len(slipped_deals) / max(1, total_deals)) * 100.0

        return {
            "slipped_deal_count": len(slipped_deals),
            "slipped_deal_value": round(total_slipped_value, 2),
            "on_track_count": len(on_track_deals),
            "on_track_value": round(total_on_track_value, 2),
            "slippage_percentage": round(slippage_rate, 2)
        }

    @staticmethod
    def calculate_sales_rep_scorecard(rep_data: Dict[str, Any]) -> Dict[str, Any]:
        quota = max(1.0, float(rep_data.get("quota", 100000.0)))
        closed_revenue = float(rep_data.get("closed_revenue", 0.0))
        attainment = (closed_revenue / quota) * 100.0

        activity_score = min(100, float(rep_data.get("calls_completed", 0)) * 2 + float(rep_data.get("emails_sent", 0)) * 0.5)
        deal_win_rate = float(rep_data.get("deals_won", 0)) / max(1, float(rep_data.get("deals_created", 1))) * 100.0

        composite_score = round((attainment * 0.50) + (deal_win_rate * 0.30) + (activity_score * 0.20), 1)

        tier = "Top Performer" if composite_score >= 100 else "Solid Performer" if composite_score >= 70 else "Needs Improvement"

        return {
            "rep_id": rep_data.get("user_id"),
            "rep_name": rep_data.get("name"),
            "attainment_percentage": round(attainment, 2),
            "win_rate_percentage": round(deal_win_rate, 2),
            "activity_score": round(activity_score, 1),
            "composite_score": composite_score,
            "performance_tier": tier
        }
""")

    # 2. backend/app/integrations/connectors/google_workspace.py
    write_file("backend/app/integrations/connectors/google_workspace.py", """from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class GoogleWorkspaceConnector:
    def __init__(self, client_id: str, client_secret: str, refresh_token: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token

    async def sync_gmail_threads(self, contact_email: str, max_results: int = 20) -> List[Dict[str, Any]]:
        # Mock Google Workspace Gmail API integration
        return [
            {
                "thread_id": f"thread_mock_{i}",
                "snippet": f"Follow-up discussion regarding contract and deliverables item #{i}",
                "from_email": contact_email,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "has_attachments": False
            }
            for i in range(1, min(max_results + 1, 6))
        ]

    async def create_calendar_event(
        self,
        summary: str,
        start_time: datetime,
        end_time: datetime,
        attendees_emails: List[str]
    ) -> Dict[str, Any]:
        return {
            "google_event_id": f"event_gcal_{int(start_time.timestamp())}",
            "summary": summary,
            "html_link": f"https://calendar.google.com/event?eid=mock_{int(start_time.timestamp())}",
            "start": start_time.isoformat(),
            "end": end_time.isoformat(),
            "attendees": [{"email": e, "response_status": "accepted"} for e in attendees_emails],
            "status": "confirmed"
        }
""")

    # 3. backend/app/integrations/connectors/microsoft_graph.py
    write_file("backend/app/integrations/connectors/microsoft_graph.py", """from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class MicrosoftGraphConnector:
    def __init__(self, tenant_id: str, client_id: str, client_secret: str):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret

    async def send_outlook_mail(
        self,
        recipient_email: str,
        subject: str,
        html_content: str
    ) -> Dict[str, Any]:
        return {
            "status": "delivered",
            "provider": "microsoft_graph_outlook",
            "recipient": recipient_email,
            "subject": subject,
            "message_id": f"msg_msft_{int(datetime.now().timestamp())}",
            "sent_at": datetime.now(timezone.utc).isoformat()
        }

    async def post_teams_card(
        self,
        webhook_url: str,
        title: str,
        text: str,
        facts: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        return {
            "status": "dispatched",
            "channel": "Microsoft Teams",
            "title": title,
            "facts": facts or {}
        }
""")

    print("Created bi_engine, google_workspace, and microsoft_graph connectors.")

if __name__ == '__main__':
    run()
