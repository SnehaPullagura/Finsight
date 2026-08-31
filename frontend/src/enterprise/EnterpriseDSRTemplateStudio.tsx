import React, { useState } from "react";
import { Layout, CheckCircle2, ShieldCheck, FileText } from "lucide-react";

export const EnterpriseDSRTemplateStudio: React.FC = () => {
  const templates = [
    { name: "Enterprise Strategic M&A", sections: "5 Modules", nda: "Required", tam: "Included", tier: "Tier 1" },
    { name: "InfoSec Heavy Compliance", sections: "5 Modules", nda: "Required", tam: "Standard", tier: "Security Focused" },
    { name: "Fast Track Commercial", sections: "3 Modules", nda: "Optional", tam: "Self-Service", tier: "Velocity" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Layout className="w-5 h-5 text-emerald-400" />
            Digital Sales Room (DSR) Enterprise Template Library
          </h3>
          <p className="text-xs text-slate-400">Pre-configured buyer room layouts with automated NDA gating and TAM collateral</p>
        </div>
      </div>

      <div className="space-y-3">
        {templates.map((t, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{t.name}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">{t.sections} • NDA: {t.nda} • TAM: {t.tam}</div>
            </div>
            <span className="text-xs font-semibold bg-emerald-950 text-emerald-400 border border-emerald-800 px-2.5 py-1 rounded-full">
              {t.tier}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
