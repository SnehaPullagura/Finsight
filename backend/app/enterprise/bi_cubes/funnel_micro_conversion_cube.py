from typing import Any, Dict, List, Optional

class FunnelMicroConversionCube:
    """
    Multi-Dimensional Sales Funnel Micro-Conversion Cube:
    Analyzes step-by-step conversion probabilities:
    Visitor -> Lead -> MQL -> SQL -> Demo -> Proposal -> Closed-Won.
    """
    @staticmethod
    def compute_funnel_health(stage_counts: Dict[str, int]) -> Dict[str, Any]:
        visitors = max(1, stage_counts.get("visitors", 10000))
        leads = stage_counts.get("leads", 500)
        mqls = stage_counts.get("mqls", 250)
        sqls = stage_counts.get("sqls", 100)
        demos = stage_counts.get("demos", 60)
        proposals = stage_counts.get("proposals", 30)
        won = stage_counts.get("closed_won", 12)

        v_to_l = round((leads / visitors) * 100.0, 2)
        l_to_m = round((mqls / max(1, leads)) * 100.0, 2)
        m_to_s = round((sqls / max(1, mqls)) * 100.0, 2)
        s_to_d = round((demos / max(1, sqls)) * 100.0, 2)
        d_to_p = round((proposals / max(1, demos)) * 100.0, 2)
        p_to_w = round((won / max(1, proposals)) * 100.0, 2)
        end_to_end = round((won / visitors) * 100.0, 3)

        return {
            "visitor_to_lead_pct": v_to_l,
            "lead_to_mql_pct": l_to_m,
            "mql_to_sql_pct": m_to_s,
            "sql_to_demo_pct": s_to_d,
            "demo_to_proposal_pct": d_to_p,
            "proposal_to_won_pct": p_to_w,
            "end_to_end_conversion_pct": end_to_end,
            "funnel_bottleneck": "MQL_TO_SQL_TRANSITION" if m_to_s < 40.0 else "DEMO_TO_PROPOSAL" if d_to_p < 50.0 else "HEALTHY_VELOCITY"
        }
