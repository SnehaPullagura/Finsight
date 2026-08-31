import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/ml_models/vector_similarity_recommender.py
    write_file("backend/app/enterprise/ml_models/vector_similarity_recommender.py", """import math
from typing import Any, Dict, List, Tuple

class VectorCosineSimilarity:
    @staticmethod
    def cosine_similarity(v1: List[float], v2: List[float]) -> float:
        if len(v1) != len(v2) or not v1:
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(v1, v2))
        norm_v1 = math.sqrt(sum(a * a for a in v1))
        norm_v2 = math.sqrt(sum(b * b for b in v2))

        if norm_v1 == 0.0 or norm_v2 == 0.0:
            return 0.0

        return round(dot_product / (norm_v1 * norm_v2), 4)

class ProductCrossSellRecommender:
    def __init__(self, product_embeddings: Dict[str, List[float]]):
        self.embeddings = product_embeddings

    def recommend_complementary_products(self, target_product_id: str, top_k: int = 3) -> List[Dict[str, Any]]:
        if target_product_id not in self.embeddings:
            return []

        target_vec = self.embeddings[target_product_id]
        scores = []

        for prod_id, vec in self.embeddings.items():
            if prod_id == target_product_id:
                continue
            sim = VectorCosineSimilarity.cosine_similarity(target_vec, vec)
            scores.append({"product_id": prod_id, "similarity_score": sim})

        scores.sort(key=lambda x: x["similarity_score"], reverse=True)
        return scores[:top_k]
""")

    # 2. backend/app/enterprise/integrations/zoom_meeting_provisioner.py
    write_file("backend/app/enterprise/integrations/zoom_meeting_provisioner.py", """import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, Optional

class ZoomMeetingProvisioner:
    def __init__(self, account_id: str, client_id: str, client_secret: str):
        self.account_id = account_id
        self.client_id = client_id
        self.client_secret = client_secret

    async def create_instant_meeting(self, topic: str, start_time_iso: str, duration_minutes: int = 30) -> Dict[str, Any]:
        meeting_id = f"zm_{int(datetime.now(timezone.utc).timestamp() * 1000)}"
        
        return {
            "id": meeting_id,
            "topic": topic,
            "type": 2, # Scheduled meeting
            "start_time": start_time_iso,
            "duration": duration_minutes,
            "join_url": f"https://zoom.us/j/{meeting_id}?pwd=secure_hash_token",
            "password": hashlib.md5(meeting_id.encode()).hexdigest()[:8],
            "status": "waiting"
        }
""")

    # 3. backend/app/enterprise/integrations/ms_teams_bot.py
    write_file("backend/app/enterprise/integrations/ms_teams_bot.py", """from typing import Any, Dict, List, Optional

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
""")

    print("Created vector similarity, zoom provisioner, and MS teams bot.")

if __name__ == '__main__':
    run()
