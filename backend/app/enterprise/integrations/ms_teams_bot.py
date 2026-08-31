from typing import Any, Dict, List, Optional

class MicrosoftTeamsCardBuilder:
    @staticmethod
    def build_deal_alert_card(deal_name: str, amount: float, rep_name: str, stage: str) -> Dict[str, Any]:
        return {
            "type": "message",
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "content": {
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "type": "AdaptiveCard",
                        "version": "1.4",
                        "body": [
                            {
                                "type": "TextBlock",
                                "size": "Large",
                                "weight": "Bolder",
                                "text": f"🎉 Deal Won: {deal_name}",
                                "color": "Good"
                            },
                            {
                                "type": "FactSet",
                                "facts": [
                                    {"title": "Deal Value:", "value": f"${amount:,.2f}"},
                                    {"title": "Sales Rep:", "value": rep_name},
                                    {"title": "Stage:", "value": stage}
                                ]
                            }
                        ]
                    }
                }
            ]
        }
