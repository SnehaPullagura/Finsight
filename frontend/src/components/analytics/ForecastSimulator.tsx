import React, { useState } from "react";
import { TrendingUp, BarChart3, Shuffle, ArrowUpRight, DollarSign } from "lucide-react";
import { api } from "../../services/api";

export const ForecastSimulator: React.FC = () => {
  const [forecast, setForecast] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);

  const sampleDeals = [
    { name: "Global Cloud Migration", value: 250000, probability: 80, stage: "negotiation" },
    { name: "AI Copilot Ops Enterprise", value: 450000, probability: 50, stage: "proposal" },
    { name: "Identity SAML SSO Platform", value: 120000, probability: 90, stage: "contract" },
    { name: "FinTech Compliance Suite", value: 180000, probability: 30, stage: "discovery" }
  ];

  const handleSimulate = async () => {
    setIsLoading(true);
    try {
      const res = await api.post("/advanced-analytics/forecast", {
        deals: sampleDeals,
        num_simulations: 2000
      });
      setForecast(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-emerald-400" />
            Monte Carlo Revenue Forecasting Engine
          </h3>
          <p className="text-xs text-slate-400">Simulate 2,000 randomized close probability distributions across your active pipeline</p>
        </div>
        <button
          onClick={handleSimulate}
          disabled={isLoading}
          className="px-4 py-2 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs rounded-lg flex items-center gap-1.5"
        >
          <Shuffle className="w-3.5 h-3.5" />
          {isLoading ? "Running Simulations..." : "Run Monte Carlo Simulation"}
        </button>
      </div>

      {forecast ? (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
            <div className="text-xs text-slate-400">Total Unweighted Pipeline</div>
            <div className="text-xl font-bold text-white mt-1">${forecast.unweighted_pipeline.toLocaleString()}</div>
            <div className="text-[11px] text-slate-500 mt-1">100% face value of open deals</div>
          </div>
          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
            <div className="text-xs text-emerald-400">Weighted Probability</div>
            <div className="text-xl font-bold text-emerald-400 mt-1">${forecast.weighted_forecast.toLocaleString()}</div>
            <div className="text-[11px] text-slate-500 mt-1">Probability-adjusted baseline</div>
          </div>
          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
            <div className="text-xs text-blue-400">P50 Expected Outcome</div>
            <div className="text-xl font-bold text-blue-400 mt-1">${forecast.monte_carlo.p50_expected.toLocaleString()}</div>
            <div className="text-[11px] text-slate-500 mt-1">50th percentile Monte Carlo</div>
          </div>
          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
            <div className="text-xs text-teal-400">P90 Optimistic Scenario</div>
            <div className="text-xl font-bold text-teal-400 mt-1">${forecast.monte_carlo.p90_optimistic.toLocaleString()}</div>
            <div className="text-[11px] text-slate-500 mt-1">90th percentile high scenario</div>
          </div>
        </div>
      ) : (
        <div className="p-8 text-center bg-slate-950/40 rounded-xl border border-dashed border-slate-800 text-slate-500 text-xs">
          Click "Run Monte Carlo Simulation" above to execute stochastic pipeline forecasting.
        </div>
      )}
    </div>
  );
};
