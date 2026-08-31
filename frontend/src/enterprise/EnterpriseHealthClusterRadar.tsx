import React, { useState } from "react";
import { Activity, ShieldCheck, TrendingUp, Users } from "lucide-react";

export const EnterpriseHealthClusterRadar: React.FC = () => {
  const clusters = [
    { cluster: "Champions & Advocates (Health 90+)", accounts: 48, arr: "$4.85M", share: "52.4%", color: "text-emerald-400" },
    { cluster: "Stable Adopters (Health 70-89)", accounts: 32, arr: "$2.95M", share: "31.8%", color: "text-blue-400" },
    { cluster: "Needs Nurturing (Health 50-69)", accounts: 10, arr: "$980K", share: "10.6%", color: "text-amber-400" },
    { cluster: "High Churn Risk (Health < 50)", accounts: 4, arr: "$480K", share: "5.2%", color: "text-red-400" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Activity className="w-5 h-5 text-emerald-400" />
            Customer Portfolio Health Cohort Clustering
          </h3>
          <p className="text-xs text-slate-400">Segmentation of ARR base by multi-variate telemetry health bands</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {clusters.map((c, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
            <span className="text-[10px] text-slate-400 font-semibold uppercase">{c.cluster}</span>
            <div className={`text-xl font-bold ${c.color}`}>{c.arr}</div>
            <span className="text-[10px] text-slate-500">{c.accounts} Accounts • {c.share}</span>
          </div>
        ))}
      </div>
    </div>
  );
};
