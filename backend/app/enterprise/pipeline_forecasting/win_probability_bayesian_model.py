from typing import Any, Dict, List, Optional

class BayesianWinProbabilityModel:
    """
    Bayesian prior-to-posterior win rate updater based on real-time deal signals:
    Prior Base Win Rate * Likelihood Ratios (Champion Verified, Infosec Signed, Budget Approved).
    """
    @staticmethod
    def calculate_posterior_probability(
        prior_stage_win_rate: float,
        has_champion: bool,
        has_economic_buyer: bool,
        is_infosec_approved: bool,
        has_budget_allocated: bool
    ) -> Dict[str, Any]:
        # Bayesian likelihood multipliers
        lr = 1.0
        if has_champion:
            lr *= 1.35
        else:
            lr *= 0.60

        if has_economic_buyer:
            lr *= 1.40
        else:
            lr *= 0.50

        if is_infosec_approved:
            lr *= 1.25

        if has_budget_allocated:
            lr *= 1.30
        else:
            lr *= 0.70

        # Prior odds
        prior_prob = prior_stage_win_rate / 100.0
        prior_odds = prior_prob / max(0.001, (1.0 - prior_prob))

        # Posterior odds
        posterior_odds = prior_odds * lr
        posterior_prob = posterior_odds / (1.0 + posterior_odds)
        final_pct = min(98.0, max(5.0, round(posterior_prob * 100.0, 1)))

        return {
            "baseline_stage_probability_pct": prior_stage_win_rate,
            "bayesian_likelihood_multiplier": round(lr, 2),
            "calibrated_posterior_win_prob_pct": final_pct,
            "confidence_band": "HIGH_CONFIDENCE_DEAL" if final_pct >= 75.0 else "MEDIUM_PROBABILITY" if final_pct >= 40.0 else "AT_RISK_OPPORTUNITY"
        }
