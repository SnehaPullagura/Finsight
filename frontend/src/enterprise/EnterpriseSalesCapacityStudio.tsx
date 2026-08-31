import React, { useState } from "react";
import { Users, TrendingUp, DollarSign, Calendar, Award } from "lucide-react";

export const EnterpriseSalesCapacityStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Users className="w-5 h-5 text-emerald-400" />
            Sales Headcount & Capacity Planning Model
          </h3>
          <p className="text-xs text-slate-400">Headcount modeling incorporating ramp time, sales cycle lag, and historical rep attrition</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Plan Approved
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">ARR Growth Target</span>
          <div className="text-2xl font-bold text-white">$15.0M</div>
          <span className="text-[10px] text-emerald-400">+100% YoY Target</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Ramped Quota per Rep</span>
          <div className="text-2xl font-bold text-white">$1,200,000</div>
          <span className="text-[10px] text-slate-400">4.5 Mo Average Ramp</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Total AE Hires Needed</span>
          <div className="text-2xl font-bold text-emerald-400">18 Reps</div>
          <span className="text-[10px] text-slate-400">Includes 15% Attrition Buffer</span>
        </div>
      </div>
    </div>
  );
};
