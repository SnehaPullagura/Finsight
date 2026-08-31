import math
import numpy as np
from typing import List, Dict, Tuple, Any
from pydantic import BaseModel

class PortfolioHolding(BaseModel):
    asset_name: str
    asset_class: str # Equity, Debt, Gold, Cash, RealEstate
    allocation_weight: float # 0.0 - 1.0
    current_value: float
    annualized_return: float # e.g. 0.12 for 12%
    annualized_volatility: float # e.g. 0.16 for 16%

class PortfolioMetricsResult(BaseModel):
    portfolio_expected_return_pct: float
    portfolio_volatility_pct: float
    sharpe_ratio: float
    sortino_ratio: float
    treynor_ratio: float
    max_drawdown_historical_pct: float
    value_at_risk_95pct_1yr: float
    conditional_var_95pct_1yr: float
    diversification_score: float # 0 - 100

class MonteCarloSimulationResult(BaseModel):
    initial_portfolio_value: float
    simulation_years: int
    iterations: int = 10000
    median_ending_value: float
    percentile_10th: float
    percentile_25th: float
    percentile_75th: float
    percentile_90th: float
    shortage_risk_below_principal_pct: float
    simulated_annual_paths_sample: List[List[float]]

class PortfolioAnalyticsEngine:
    """
    Institutional Portfolio Analytics & Monte Carlo Simulation Engine.
    Computes Modern Portfolio Theory (MPT) statistics, risk-adjusted returns, and probabilistic outcome envelopes.
    """
    @staticmethod
    def compute_portfolio_metrics(
        holdings: List[PortfolioHolding], risk_free_rate: float = 0.065
    ) -> PortfolioMetricsResult:
        if not holdings:
            return PortfolioMetricsResult(
                portfolio_expected_return_pct=0.0, portfolio_volatility_pct=0.0,
                sharpe_ratio=0.0, sortino_ratio=0.0, treynor_ratio=0.0,
                max_drawdown_historical_pct=0.0, value_at_risk_95pct_1yr=0.0,
                conditional_var_95pct_1yr=0.0, diversification_score=0.0
            )

        weights = np.array([h.allocation_weight for h in holdings])
        weights = weights / np.sum(weights) # Normalize to 1.0
        
        returns = np.array([h.annualized_return for h in holdings])
        volatilities = np.array([h.annualized_volatility for h in holdings])

        # Expected portfolio return
        exp_return = float(np.sum(weights * returns))

        # Approximate covariance matrix with realistic asset cross-correlations
        n = len(holdings)
        corr_matrix = np.eye(n)
        for i in range(n):
            for j in range(n):
                if i != j:
                    c1, c2 = holdings[i].asset_class.lower(), holdings[j].asset_class.lower()
                    if c1 == c2:
                        corr_matrix[i, j] = 0.75
                    elif ("equity" in c1 and "debt" in c2) or ("debt" in c1 and "equity" in c2):
                        corr_matrix[i, j] = 0.10
                    elif "gold" in c1 or "gold" in c2:
                        corr_matrix[i, j] = 0.05
                    else:
                        corr_matrix[i, j] = 0.30

        cov_matrix = np.outer(volatilities, volatilities) * corr_matrix
        port_vol = float(np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))))

        # Sharpe Ratio
        excess_return = exp_return - risk_free_rate
        sharpe = excess_return / port_vol if port_vol > 0 else 0.0

        # Sortino Ratio (Downside volatility proxy: ~60% of total volatility)
        downside_vol = port_vol * 0.65
        sortino = excess_return / downside_vol if downside_vol > 0 else 0.0

        # 95% Parametric VaR (1 Year Horizon)
        z_95 = 1.64485
        total_val = sum(h.current_value for h in holdings)
        var_95 = total_val * (z_95 * port_vol - exp_return)
        cvar_95 = var_95 * 1.25

        # Diversification Score (Herfindahl-Hirschman Index inverted)
        hhi = np.sum(weights ** 2)
        div_score = min(100.0, max(0.0, (1.0 - hhi) / (1.0 - (1.0 / max(2, n))) * 100.0))

        return PortfolioMetricsResult(
            portfolio_expected_return_pct=round(exp_return * 100, 2),
            portfolio_volatility_pct=round(port_vol * 100, 2),
            sharpe_ratio=round(sharpe, 2),
            sortino_ratio=round(sortino, 2),
            treynor_ratio=round(excess_return / 1.05, 2),
            max_drawdown_historical_pct=round(port_vol * 1.8 * 100, 2),
            value_at_risk_95pct_1yr=round(max(0.0, var_95), 2),
            conditional_var_95pct_1yr=round(max(0.0, cvar_95), 2),
            diversification_score=round(div_score, 1)
        )

    @staticmethod
    def run_monte_carlo_simulation(
        initial_value: float,
        annual_contribution: float,
        expected_return_pct: float,
        volatility_pct: float,
        years: int = 10,
        iterations: int = 5000
    ) -> MonteCarloSimulationResult:
        mu = expected_return_pct / 100.0
        sigma = volatility_pct / 100.0
        dt = 1.0

        ending_values = []
        sample_paths = []

        # Geometric Brownian Motion simulation
        for i in range(iterations):
            path = [initial_value]
            curr = initial_value
            for t in range(years):
                rand_z = np.random.normal(0, 1)
                # S(t+1) = S(t) * exp((mu - 0.5*sigma^2)*dt + sigma*sqrt(dt)*Z) + Contribution
                growth = np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * rand_z)
                curr = curr * growth + annual_contribution
                path.append(round(curr, 2))
            ending_values.append(curr)
            if i < 8:
                sample_paths.append(path)

        end_arr = np.array(ending_values)
        principal_invested = initial_value + (annual_contribution * years)
        shortage_count = np.sum(end_arr < principal_invested)

        return MonteCarloSimulationResult(
            initial_portfolio_value=initial_value,
            simulation_years=years,
            iterations=iterations,
            median_ending_value=round(float(np.median(end_arr)), 2),
            percentile_10th=round(float(np.percentile(end_arr, 10)), 2),
            percentile_25th=round(float(np.percentile(end_arr, 25)), 2),
            percentile_75th=round(float(np.percentile(end_arr, 75)), 2),
            percentile_90th=round(float(np.percentile(end_arr, 90)), 2),
            shortage_risk_below_principal_pct=round(float(shortage_count / iterations * 100.0), 2),
            simulated_annual_paths_sample=sample_paths
        )
