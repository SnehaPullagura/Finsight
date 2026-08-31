import React, { useState } from "react";
import { TrendingUp, BarChart2, DollarSign, ArrowUpRight, ShieldCheck } from "lucide-react";

export const EnterpriseRevenueForecastMatrix: React.FC = () => {
  const forecastTiers = [
    { category: "Closed Won Bookings", amount: 1450000, confidence: "100%", risk: "Zero", color: "text-emerald-400" },
    { category: "Commit Forecast", amount: 620000, confidence: "90%", risk: "Low", color: "text-blue-400" },
    { category: "Best Case Scenario", amount: 480000, confidence: "60%", risk: "Moderate", color: "text-amber-400" },
    { category: "Open Pipeline", amount: 950000, confidence: "35%", risk: "High", color: "text-purple-400" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <BarChart2 className="w-5 h-5 text-emerald-400" />
            Quarterly Revenue Forecast & Weighted Commit Matrix
          </h3>
          <p className="text-xs text-slate-400">Monte Carlo weighted probability analysis with quota gap tracking</p>
        </div>
        <div className="text-right">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Quarter Target</span>
          <div className="text-xl font-bold text-white">$2,500,000</div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {forecastTiers.map((tier, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
            <span className="text-[11px] text-slate-400 font-medium">{tier.category}</span>
            <div className={`text-xl font-bold ${tier.color}`}>${tier.amount.toLocaleString()}</div>
            <div className="text-[10px] text-slate-500 flex justify-between pt-1">
              <span>Confidence: {tier.confidence}</span>
              <span>Risk: {tier.risk}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
