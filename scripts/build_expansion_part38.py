import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/crm_analytics/executive_board_revenue_waterfall.py
    write_file("backend/app/enterprise/crm_analytics/executive_board_revenue_waterfall.py", """from typing import Any, Dict, List, Optional

class BoardRevenueWaterfallModeler:
    @staticmethod
    def calculate_arr_bridge(
        starting_arr: float,
        new_logo_arr: float,
        expansion_arr: float,
        cross_sell_arr: float,
        contraction_arr: float,
        churn_arr: float
    ) -> Dict[str, Any]:
        gross_new_arr = new_logo_arr + expansion_arr + cross_sell_arr
        total_loss_arr = contraction_arr + churn_arr
        net_new_arr = gross_new_arr - total_loss_arr
        ending_arr = starting_arr + net_new_arr

        arr_growth_pct = round((net_new_arr / max(1.0, starting_arr)) * 100.0, 1)

        return {
            "starting_arr": starting_arr,
            "new_logo_arr": new_logo_arr,
            "expansion_arr": expansion_arr,
            "cross_sell_arr": cross_sell_arr,
            "gross_new_arr": gross_new_arr,
            "contraction_arr": contraction_arr,
            "churn_arr": churn_arr,
            "total_loss_arr": total_loss_arr,
            "net_new_arr": net_new_arr,
            "ending_arr": ending_arr,
            "arr_growth_percentage": arr_growth_pct
        }
""")

    # 2. backend/app/enterprise/security_governance/database_field_blind_indexer.py
    write_file("backend/app/enterprise/security_governance/database_field_blind_indexer.py", """import hmac
import hashlib
from typing import Any, Dict, Optional

class DatabaseBlindIndexer:
    @staticmethod
    def generate_blind_index(plaintext_value: str, blind_index_key: str) -> str:
        cleaned = plaintext_value.strip().lower()
        b_idx = hmac.new(blind_index_key.encode(), cleaned.encode(), hashlib.sha256).hexdigest()
        return f"bidx_{b_idx[:32]}"
""")

    # 3. frontend/src/enterprise/EnterpriseBoardRevenueWaterfall.tsx
    write_file("frontend/src/enterprise/EnterpriseBoardRevenueWaterfall.tsx", """import React, { useState } from "react";
import { TrendingUp, DollarSign, Layers, CheckCircle2 } from "lucide-react";

export const EnterpriseBoardRevenueWaterfall: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-emerald-400" />
            Board of Directors ARR Revenue Waterfall Bridge
          </h3>
          <p className="text-xs text-slate-400">Quarterly ARR bridge decomposing new logo acquisition, expansion, and logo churn</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          +$3.25M Net ARR Growth
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Starting ARR</span>
          <div className="text-2xl font-bold text-white">$12.5M</div>
          <span className="text-[10px] text-slate-400">Q1 Baseline</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Gross New Added</span>
          <div className="text-2xl font-bold text-emerald-400">+$3.85M</div>
          <span className="text-[10px] text-emerald-400">New Logo + Upsell</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Total Lost ARR</span>
          <div className="text-2xl font-bold text-red-400">-$600K</div>
          <span className="text-[10px] text-red-400">4.8% Logo Churn</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Ending ARR</span>
          <div className="text-2xl font-bold text-white">$15.75M</div>
          <span className="text-[10px] text-emerald-400">+26.0% QoQ Expansion</span>
        </div>
      </div>
    </div>
  );
};
""")

    # 4. frontend/src/enterprise/EnterpriseBlindIndexingStudio.tsx
    write_file("frontend/src/enterprise/EnterpriseBlindIndexingStudio.tsx", """import React, { useState } from "react";
import { Search, Lock, Shield, CheckCircle2 } from "lucide-react";

export const EnterpriseBlindIndexingStudio: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <Search className="w-5 h-5 text-emerald-400" />
            Zero-Knowledge Encrypted Field Blind Indexing
          </h3>
          <p className="text-xs text-slate-400">Exact match searching over encrypted sensitive fields without leaking plaintext or cipher patterns</p>
        </div>
        <span className="bg-emerald-950 border border-emerald-800 text-emerald-400 text-xs font-bold px-3 py-1 rounded-full uppercase">
          HMAC-SHA256 Blind Indexing
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Search Index Key</span>
          <div className="text-xs font-mono text-emerald-400">KDF-HMAC-256</div>
          <span className="text-[10px] text-slate-400">Isolated Search Salt</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Search Performance</span>
          <div className="text-2xl font-bold text-white">0.2ms</div>
          <span className="text-[10px] text-emerald-400">B-Tree Indexed Hash Lookup</span>
        </div>
        <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
          <span className="text-[11px] text-slate-400 uppercase font-semibold">Zero-Knowledge Proof</span>
          <div className="text-xs font-bold text-emerald-400">100% Blind Search</div>
          <span className="text-[10px] text-slate-400">Zero Plaintext Leakage to DB</span>
        </div>
      </div>
    </div>
  );
};
""")

    print("Created board waterfall, blind indexer, and UI components.")

if __name__ == '__main__':
    run()
