import React, { useEffect, useState } from "react";
import { HeartHandshake, ShieldAlert, CheckCircle2 } from "lucide-react";
import { api } from "../../services/api";
import { CustomerSuccessPlan } from "../../types";

export const CustomerSuccessPage: React.FC = () => {
  const [plans, setPlans] = useState<CustomerSuccessPlan[]>([]);

  useEffect(() => {
    api.getSuccessPlans().then(res => setPlans(res.data)).catch(console.error);
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-bold text-slate-900">Customer Success & Health</h1>
        <p className="text-xs text-slate-500">Client health scores, onboarding tracks, and churn risk mitigation</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {plans.map(p => (
          <div key={p.id} className="bg-white p-5 rounded-xl border border-slate-200 shadow-2xs space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-xs font-bold text-slate-900">Health Score: {p.health_score}/100</span>
              <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold uppercase ${p.health_grade === 'good' ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'}`}>
                {p.health_grade}
              </span>
            </div>
            <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
              <div className={`h-full ${p.health_score > 70 ? 'bg-emerald-500' : 'bg-amber-500'} rounded-full`} style={{ width: `${p.health_score}%` }}></div>
            </div>
            <div className="text-[11px] text-slate-500">Milestones: {p.milestones?.length || 0} tracks configured</div>
          </div>
        ))}
        {plans.length === 0 && <div className="p-8 col-span-full text-center text-xs text-slate-400 bg-white rounded-xl border border-slate-200">Customer success plans active.</div>}
      </div>
    </div>
  );
};
