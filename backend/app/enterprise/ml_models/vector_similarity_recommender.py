import math
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
