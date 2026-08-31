import React, { useState } from "react";
import { Building, DollarSign, Users, Award, Shield, CheckCircle2, TrendingUp, AlertCircle, Phone, Mail } from "lucide-react";

export const EnterpriseCustomer360View: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-emerald-950 border border-emerald-800 flex items-center justify-center text-emerald-400 font-bold text-lg">
            ST
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-xl font-bold text-white">Stark Industries Global</h2>
              <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-[10px] font-bold px-2 py-0.5 rounded-full uppercase">Enterprise Tier 1</span>
            </div>
            <p className="text-xs text-slate-400">Technology & Aerospace • New York, USA • 1,200 Employees</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <div className="text-right">
            <span className="text-[11px] text-slate-400 font-medium">Customer Health Score</span>
            <div className="text-xl font-bold text-emerald-400">94 / 100 (Grade A)</div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Annual Run Rate (ARR)</span>
          <div className="text-xl font-bold text-white mt-1">$450,000</div>
          <span className="text-[10px] text-emerald-400">Auto-Renews: Dec 2026</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Lifetime Value (LTV)</span>
          <div className="text-xl font-bold text-white mt-1">$1,250,000</div>
          <span className="text-[10px] text-emerald-400">3-Year Retention</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Active Support Tickets</span>
          <div className="text-xl font-bold text-white mt-1">0 Open</div>
          <span className="text-[10px] text-emerald-400">100% SLA Compliant</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Stakeholder Count</span>
          <div className="text-xl font-bold text-white mt-1">8 Key Contacts</div>
          <span className="text-[10px] text-slate-400">Executive Sponsor Aligned</span>
        </div>
      </div>
    </div>
  );
};
