import React, { useState } from "react";
import { Globe, Shield, Lock, CheckCircle2, AlertTriangle } from "lucide-react";

export const EnterpriseIPGeofencingStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Globe className="w-5 h-5 text-emerald-400" />
            Zero-Trust IP Geofencing & Country Allowlisting
          </h3>
          <p className="text-xs text-slate-400">Restrict administrative access to authorized IP CIDR blocks and sovereign jurisdictions</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Zero-Trust Guard Active
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Allowed Sovereign Regions</span>
          <div className="text-xs font-bold text-white">United States (US), European Union (EU)</div>
          <span className="text-[10px] text-emerald-400">Strict Sovereignty</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Corporate VPN CIDRs</span>
          <div className="text-xs font-mono text-white">10.100.0.0/16, 172.16.0.0/12</div>
          <span className="text-[10px] text-emerald-400">Corporate Subnets</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Blocked Geo Attempts</span>
          <div className="text-xs font-bold text-slate-300">0 Breaches in 30 Days</div>
          <span className="text-[10px] text-emerald-400">100% Blocked</span>
        </div>
      </div>
    </div>
  );
};
