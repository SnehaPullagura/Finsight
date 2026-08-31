import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/domain_handlers/deduplication_fuzzy_matcher.py
    write_file("backend/app/enterprise/domain_handlers/deduplication_fuzzy_matcher.py", """import re
from typing import Any, Dict, List, Tuple

class FuzzyStringDistance:
    @staticmethod
    def levenshtein_ratio(s1: str, s2: str) -> float:
        s1 = s1.lower().strip()
        s2 = s2.lower().strip()
        if s1 == s2:
            return 1.0
        if not s1 or not s2:
            return 0.0

        rows = len(s1) + 1
        cols = len(s2) + 1
        dist = [[0 for _ in range(cols)] for _ in range(rows)]

        for i in range(rows):
            dist[i][0] = i
        for j in range(cols):
            dist[0][j] = j

        for i in range(1, rows):
            for j in range(1, cols):
                cost = 0 if s1[i - 1] == s2[j - 1] else 1
                dist[i][j] = min(
                    dist[i - 1][j] + 1,      # deletion
                    dist[i][j - 1] + 1,      # insertion
                    dist[i - 1][j - 1] + cost # substitution
                )

        max_len = max(len(s1), len(s2))
        return round(1.0 - (dist[rows - 1][cols - 1] / float(max_len)), 4)

class EnterpriseFuzzyDeduplicator:
    @staticmethod
    def find_duplicate_contacts(
        target_contact: Dict[str, Any],
        candidate_pool: List[Dict[str, Any]],
        threshold: float = 0.80
    ) -> List[Dict[str, Any]]:
        matches = []
        t_email = target_contact.get("email", "").lower().strip()
        t_name = f"{target_contact.get('first_name', '')} {target_contact.get('last_name', '')}".strip()

        for c in candidate_pool:
            if c.get("id") == target_contact.get("id"):
                continue

            c_email = c.get("email", "").lower().strip()
            c_name = f"{c.get('first_name', '')} {c.get('last_name', '')}".strip()

            # Exact email match
            if t_email and c_email and t_email == c_email:
                matches.append({"candidate": c, "confidence": 1.0, "match_type": "exact_email"})
                continue

            # Fuzzy name match
            ratio = FuzzyStringDistance.levenshtein_ratio(t_name, c_name)
            if ratio >= threshold:
                matches.append({"candidate": c, "confidence": ratio, "match_type": "fuzzy_name"})

        return sorted(matches, key=lambda x: x["confidence"], reverse=True)
""")

    # 2. backend/app/enterprise/domain_handlers/territory_hierarchies.py
    write_file("backend/app/enterprise/domain_handlers/territory_hierarchies.py", """from typing import Any, Dict, List, Optional

class TerritoryNode:
    def __init__(self, node_id: str, name: str, level: str, parent_id: Optional[str] = None):
        self.node_id = node_id
        self.name = name
        self.level = level # Global, Theater, Region, Area, Territory
        self.parent_id = parent_id
        self.children = []
        self.assigned_quota = 0.0

class EnterpriseTerritoryHierarchy:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node: TerritoryNode):
        self.nodes[node.node_id] = node
        if node.parent_id and node.parent_id in self.nodes:
            self.nodes[node.parent_id].children.append(node)

    def calculate_rollup_quota(self, node_id: str) -> float:
        if node_id not in self.nodes:
            return 0.0
        node = self.nodes[node_id]
        if not node.children:
            return node.assigned_quota
        return node.assigned_quota + sum(self.calculate_rollup_quota(c.node_id) for c in node.children)
""")

    # 3. frontend/src/enterprise/EnterpriseAnalyticsWorkbench.tsx
    write_file("frontend/src/enterprise/EnterpriseAnalyticsWorkbench.tsx", """import React, { useState } from "react";
import { BarChart3, LineChart, PieChart, Activity, DollarSign, Users, Award, TrendingUp } from "lucide-react";
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

const MONTHLY_REVENUE_TREND = [
  { month: "Jan", arr: 1200000, mrr: 100000, expansion: 15000, churn: 2000 },
  { month: "Feb", arr: 1350000, mrr: 112500, expansion: 18000, churn: 1500 },
  { month: "Mar", arr: 1520000, mrr: 126600, expansion: 22000, churn: 3000 },
  { month: "Apr", arr: 1780000, mrr: 148300, expansion: 29000, churn: 1000 },
  { month: "May", arr: 2100000, mrr: 175000, expansion: 35000, churn: 2500 },
  { month: "Jun", arr: 2450000, mrr: 204100, expansion: 42000, churn: 1800 }
];

export const EnterpriseAnalyticsWorkbench: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <span className="text-xs text-slate-400 font-medium uppercase tracking-wider">Annual Run Rate (ARR)</span>
          <div className="text-2xl font-bold text-white mt-1">$2,450,000</div>
          <div className="text-xs text-emerald-400 mt-2 font-medium">↑ +104.1% YoY Growth</div>
        </div>
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <span className="text-xs text-slate-400 font-medium uppercase tracking-wider">Net Revenue Retention (NRR)</span>
          <div className="text-2xl font-bold text-white mt-1">128.4%</div>
          <div className="text-xs text-emerald-400 mt-2 font-medium">Top Quartile SaaS Benchmark</div>
        </div>
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <span className="text-xs text-slate-400 font-medium uppercase tracking-wider">Gross Logo Retention</span>
          <div className="text-2xl font-bold text-white mt-1">97.2%</div>
          <div className="text-xs text-emerald-400 mt-2 font-medium">0.3% Churn per Quarter</div>
        </div>
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl">
          <span className="text-xs text-slate-400 font-medium uppercase tracking-wider">Sales Velocity Index</span>
          <div className="text-2xl font-bold text-white mt-1">42 Days</div>
          <div className="text-xs text-emerald-400 mt-2 font-medium">↓ -12 Days Faster Cycle</div>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 p-6 rounded-xl shadow-xl space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-emerald-400" />
              ARR Waterfall & Monthly Expansion Trajectory
            </h3>
            <p className="text-xs text-slate-400">Quarterly growth trajectory with new bookings, account expansions, and churn offsets</p>
          </div>
        </div>

        <div className="h-72 bg-slate-950 p-4 rounded-xl border border-slate-800">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={MONTHLY_REVENUE_TREND}>
              <defs>
                <linearGradient id="colorArr" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.4}/>
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="month" stroke="#64748b" fontSize={11} />
              <YAxis stroke="#64748b" fontSize={11} tickFormatter={val => `$${val/1000000}M`} />
              <Tooltip
                contentStyle={{ backgroundColor: "#0f172a", borderColor: "#334155", borderRadius: "8px", fontSize: "11px" }}
              />
              <Area type="monotone" dataKey="arr" stroke="#10b981" fillOpacity={1} fill="url(#colorArr)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};
""")

    print("Created deduplication fuzzy matcher, territory hierarchies, and analytics workbench.")

if __name__ == '__main__':
    run()
