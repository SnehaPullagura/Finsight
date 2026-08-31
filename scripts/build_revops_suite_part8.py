import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. frontend/src/enterprise/EnterpriseASC606ScheduleStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseASC606ScheduleStudio.tsx", """import React, { useState } from "react";
import { Calculator, DollarSign, Calendar, CheckCircle2, FileText } from "lucide-react";

export const EnterpriseASC606ScheduleStudio: React.FC = () => {
  const schedules = [
    { period: "2026-09", rec: "$20,833.33", def: "$229,166.67", status: "Recognized" },
    { period: "2026-10", rec: "$20,833.33", def: "$208,333.34", status: "Scheduled" },
    { period: "2026-11", rec: "$20,833.33", def: "$187,500.01", status: "Scheduled" },
    { period: "2026-12", rec: "$20,833.33", def: "$166,666.68", status: "Scheduled" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Calculator className="w-5 h-5 text-emerald-400" />
            ASC 606 / IFRS 15 Revenue Amortization Schedule
          </h3>
          <p className="text-xs text-slate-400">Straight-line and multi-element revenue recognition engine for multi-year contracts</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          ASC 606 Compliant
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Total Contract Value</span>
          <div className="text-2xl font-bold text-white">$250,000.00</div>
          <span className="text-[10px] text-slate-400">12-Month Enterprise SaaS Term</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Monthly Amortization</span>
          <div className="text-2xl font-bold text-emerald-400">$20,833.33 / Mo</div>
          <span className="text-[10px] text-emerald-400">Straight-Line Over Time</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Ending Deferred Balance</span>
          <div className="text-2xl font-bold text-white">$229,166.67</div>
          <span className="text-[10px] text-slate-400">Auto-Balancing General Ledger</span>
        </div>
      </div>

      <div className="space-y-3">
        {schedules.map((s, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">Period: {s.period}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Recognized: <span className="text-emerald-400 font-bold">{s.rec}</span> • Ending Deferred: {s.def}</div>
            </div>
            <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${
              s.status === "Recognized" ? "bg-emerald-950 text-emerald-400 border border-emerald-800" : "bg-slate-800 text-slate-400"
            }`}>
              {s.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    # 2. frontend/src/enterprise/EnterpriseTerritoryOptimizerStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseTerritoryOptimizerStudio.tsx", """import React, { useState } from "react";
import { Globe, Users, Target, CheckCircle2, RefreshCw } from "lucide-react";

export const EnterpriseTerritoryOptimizerStudio: React.FC = () => {
  const territories = [
    { id: "TERR-1", name: "US West - Enterprise", accounts: 42, tam: "$8.4M", variance: "+2.1%", rep: "Alex Vance" },
    { id: "TERR-2", name: "US East - Financial Services", accounts: 38, tam: "$8.2M", variance: "-0.5%", rep: "Sarah Connor" },
    { id: "TERR-3", name: "EMEA & Strategic Accounts", accounts: 35, tam: "$8.6M", variance: "+4.2%", rep: "John Wick" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Globe className="w-5 h-5 text-emerald-400" />
            Enterprise Territory Optimizer & TAM Workload Equalizer
          </h3>
          <p className="text-xs text-slate-400">Algorithmic territory balancing ensuring equitable quota capacity across sales teams</p>
        </div>
        <button className="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-500 text-white px-3 py-1.5 rounded-lg text-xs font-semibold shadow transition-colors">
          <RefreshCw className="w-4 h-4" />
          Rebalance Territories
        </button>
      </div>

      <div className="space-y-3">
        {territories.map((t, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{t.name} ({t.id})</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Assigned Rep: {t.rep} • {t.accounts} Accounts • Total TAM: <span className="text-emerald-400 font-bold">{t.tam}</span></div>
            </div>
            <div className="text-right">
              <span className="text-xs font-bold text-emerald-400">{t.variance} Variance</span>
              <span className="text-[10px] text-slate-500 block">Balanced Territory</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    # 3. frontend/src/enterprise/EnterprisePartnerDealRegStudio.tsx
    write_file("frontend/src/enterprise/EnterprisePartnerDealRegStudio.tsx", """import React, { useState } from "react";
import { Handshake, Award, ShieldCheck, CheckCircle2, DollarSign } from "lucide-react";

export const EnterprisePartnerDealRegStudio: React.FC = () => {
  const registrations = [
    { partner: "Accenture Digital", account: "Stark Industries", deal: "$450,000", margin: "15%", status: "Exclusivity Approved (90d)" },
    { partner: "Deloitte Consulting", account: "Wayne Enterprises", deal: "$280,000", margin: "15%", status: "Exclusivity Approved (90d)" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Handshake className="w-5 h-5 text-emerald-400" />
            Global SI & Co-Sell Deal Registration Portal
          </h3>
          <p className="text-xs text-slate-400">Automated conflict collision checks and 90-day lead exclusivity protection</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Portal Active
        </span>
      </div>

      <div className="space-y-3">
        {registrations.map((r, idx) => (
          <div key={idx} className="bg-slate-950 border border-slate-800 p-4 rounded-xl flex items-center justify-between">
            <div>
              <div className="text-xs font-bold text-white">{r.partner} → {r.account}</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Registered Value: {r.deal} • Partner Incentive Margin: <span className="text-emerald-400 font-bold">{r.margin}</span></div>
            </div>
            <span className="text-xs font-semibold bg-emerald-950 text-emerald-400 border border-emerald-800 px-2.5 py-1 rounded-full">
              {r.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
""")

    # 4. frontend/src/enterprise/EnterpriseSOXControlStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseSOXControlStudio.tsx", """import React, { useState } from "react";
import { ShieldCheck, Lock, CheckCircle2, AlertCircle } from "lucide-react";

export const EnterpriseSOXControlStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            SOX ITGC Separation of Duties & Change Control Auditor
          </h3>
          <p className="text-xs text-slate-400">Automated validation of production release approvals and financial audit trails</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          100% SOX Compliant
        </span>
      </div>

      <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold text-white">Continuous ITGC Auditing Engine</span>
          <span className="text-xs text-emerald-400 font-semibold">Live Monitoring</span>
        </div>
        <div className="space-y-2 text-xs text-slate-300">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>Separation of Duties (SoD) enforced on all revenue configuration mutations</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>HMAC SHA-256 cryptographic signatures verified across 100% of audit ledger rows</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>Automated rollback test plans verified for every production deploy</span>
          </div>
        </div>
      </div>
    </div>
  );
};
""")

    # 5. frontend/src/enterprise/EnterpriseCallTranscriptTopicStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseCallTranscriptTopicStudio.tsx", """import React, { useState } from "react";
import { Mic, Sparkles, MessageSquare, CheckCircle2, TrendingUp } from "lucide-react";

export const EnterpriseCallTranscriptTopicStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Mic className="w-5 h-5 text-emerald-400" />
            AI Conversation Intelligence & Talk-to-Listen Cadence
          </h3>
          <p className="text-xs text-slate-400">NLP topic extraction and rep talk-time ratio analysis from recorded sales meetings</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          Optimal 44% / 56%
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Rep Talk Ratio</span>
          <div className="text-2xl font-bold text-emerald-400">44.2%</div>
          <span className="text-[10px] text-slate-400">Target Benchmark: &lt; 48%</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Customer Talk Ratio</span>
          <div className="text-2xl font-bold text-white">55.8%</div>
          <span className="text-[10px] text-emerald-400">High Engagement Discovery</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Competitor Mentions</span>
          <div className="text-2xl font-bold text-amber-400">2 Mentions</div>
          <span className="text-[10px] text-slate-400">HubSpot & Salesforce CPQ</span>
        </div>
      </div>
    </div>
  );
};
""")

    # 6. frontend/src/enterprise/EnterpriseDealDeskStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseDealDeskStudio.tsx", """import React, { useState } from "react";
import { Package, ShieldCheck, DollarSign, CheckCircle2 } from "lucide-react";

export const EnterpriseDealDeskStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Package className="w-5 h-5 text-emerald-400" />
            Executive Deal Desk & Enterprise Bundle Configurator
          </h3>
          <p className="text-xs text-slate-400">Pre-approved enterprise licensing packages with TAM and 24x7 mission-critical SLA add-ons</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          82.5% Gross Margin
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Core Platform</span>
          <div className="text-2xl font-bold text-white">$120,000</div>
          <span className="text-[10px] text-slate-400">100 Enterprise Seats</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Dedicated TAM</span>
          <div className="text-2xl font-bold text-white">$35,000</div>
          <span className="text-[10px] text-emerald-400">Named Lead Architect</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Premium SLA</span>
          <div className="text-2xl font-bold text-white">$18,000</div>
          <span className="text-[10px] text-slate-400">15-Min Response Guarantee</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Total ACV</span>
          <div className="text-2xl font-bold text-emerald-400">$173,000</div>
          <span className="text-[10px] text-emerald-400">Pre-Approved Bundle</span>
        </div>
      </div>
    </div>
  );
};
""")

    print("Frontend UI studios created successfully.")

if __name__ == "__main__":
    run()
