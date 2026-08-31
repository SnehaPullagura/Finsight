import React, { useState } from "react";
import { Monitor, Share2, FileText, CheckCircle2, Lock } from "lucide-react";

export const EnterpriseDigitalSalesRoomStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Monitor className="w-5 h-5 text-emerald-400" />
            Digital Sales Room (DSR) & Buyer Experience Portal
          </h3>
          <p className="text-xs text-slate-400">Curated executive deal microsite with mutual action plans, NDA gating, and proposal decks</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Portal Published
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Buyer Engagement Time</span>
          <div className="text-2xl font-bold text-emerald-400">42 Mins Total</div>
          <span className="text-[10px] text-emerald-400">High Intent Session</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Stakeholders Active</span>
          <div className="text-2xl font-bold text-white">4 Decision Makers</div>
          <span className="text-[10px] text-slate-400">VP, Security Lead, Legal, CFO</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Mutual Milestones</span>
          <div className="text-2xl font-bold text-white">5 of 6 Done</div>
          <span className="text-[10px] text-emerald-400">83.3% MAP Completed</span>
        </div>
      </div>
    </div>
  );
};
