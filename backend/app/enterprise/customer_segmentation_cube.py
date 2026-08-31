from typing import Any, Dict, List, Optional
from collections import defaultdict

class CustomerSegmentationCube:
    @staticmethod
    def calculate_rfm_scores(customer_orders: List[Dict[str, Any]], snapshot_date: Optional[str] = None) -> List[Dict[str, Any]]:
        # Recency, Frequency, Monetary (RFM) Segmentation
        customer_groups = defaultdict(lambda: {"orders": [], "total_spent": 0.0, "last_order_days": 999})

        for order in customer_orders:
            cid = order.get("company_id") or order.get("contact_id", "anon")
            amount = float(order.get("amount", 0.0))
            days_ago = int(order.get("days_ago", 30))

            customer_groups[cid]["orders"].append(order)
            customer_groups[cid]["total_spent"] += amount
            customer_groups[cid]["last_order_days"] = min(customer_groups[cid]["last_order_days"], days_ago)

        rfm_results = []
        for cid, data in customer_groups.items():
            r_score = 5 if data["last_order_days"] <= 14 else 4 if data["last_order_days"] <= 30 else 3 if data["last_order_days"] <= 60 else 2 if data["last_order_days"] <= 90 else 1
            f_score = 5 if len(data["orders"]) >= 10 else 4 if len(data["orders"]) >= 5 else 3 if len(data["orders"]) >= 3 else 2 if len(data["orders"]) >= 2 else 1
            m_score = 5 if data["total_spent"] >= 100000 else 4 if data["total_spent"] >= 50000 else 3 if data["total_spent"] >= 20000 else 2 if data["total_spent"] >= 5000 else 1

            composite = f"{r_score}{f_score}{m_score}"
            segment = "Champions" if r_score >= 4 and f_score >= 4 and m_score >= 4 else "Loyal Customers" if f_score >= 3 else "At Risk" if r_score <= 2 and m_score >= 3 else "Hibernating"

            rfm_results.append({
                "customer_id": cid,
                "recency_days": data["last_order_days"],
                "frequency_count": len(data["orders"]),
                "monetary_total": round(data["total_spent"], 2),
                "rfm_score": composite,
                "segment": segment
            })

        return sorted(rfm_results, key=lambda x: x["monetary_total"], reverse=True)
