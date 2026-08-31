import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/workflow_engine/event_stream_processor.py
    write_file("backend/app/enterprise/workflow_engine/event_stream_processor.py", """import asyncio
import json
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

class EventStreamEnvelope:
    def __init__(self, event_id: str, topic: str, tenant_id: str, payload: Dict[str, Any]):
        self.event_id = event_id
        self.topic = topic
        self.tenant_id = tenant_id
        self.payload = payload
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.retry_count = 0

class EnterpriseEventBroker:
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        self.subscribers = {}
        self.dead_letter_queue = []
        self.journal = []

    def subscribe(self, topic: str, handler: Callable[[EventStreamEnvelope], Any]):
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(handler)

    async def publish(self, topic: str, tenant_id: str, payload: Dict[str, Any]) -> str:
        evt_id = f"evt_{int(datetime.now(timezone.utc).timestamp() * 1000)}"
        envelope = EventStreamEnvelope(evt_id, topic, tenant_id, payload)
        self.journal.append(envelope)

        handlers = self.subscribers.get(topic, [])
        for h in handlers:
            try:
                res = await h(envelope) if asyncio.iscoroutinefunction(h) else h(envelope)
            except Exception as e:
                envelope.retry_count += 1
                if envelope.retry_count > self.max_retries:
                    self.dead_letter_queue.append({"envelope": envelope, "error": str(e)})

        return evt_id
""")

    # 2. backend/app/enterprise/workflow_engine/ast_expression_parser.py
    write_file("backend/app/enterprise/workflow_engine/ast_expression_parser.py", """import ast
import operator
from typing import Any, Dict

class SafeASTExpressionParser:
    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Eq: operator.eq,
        ast.NotEq: operator.ne,
        ast.Lt: operator.lt,
        ast.LtE: operator.le,
        ast.Gt: operator.gt,
        ast.GtE: operator.ge,
        ast.And: lambda a, b: a and b,
        ast.Or: lambda a, b: a or b,
        ast.Not: operator.not_
    }

    @staticmethod
    def evaluate(expression: str, context: Dict[str, Any]) -> Any:
        try:
            tree = ast.parse(expression, mode='eval')
            return SafeASTExpressionParser._eval_node(tree.body, context)
        except Exception as e:
            raise ValueError(f"Failed to evaluate safe expression '{expression}': {str(e)}")

    @staticmethod
    def _eval_node(node: ast.AST, context: Dict[str, Any]) -> Any:
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Name):
            if node.id in context:
                return context[node.id]
            raise NameError(f"Undefined variable in workflow rule: '{node.id}'")
        elif isinstance(node, ast.BinOp):
            left = SafeASTExpressionParser._eval_node(node.left, context)
            right = SafeASTExpressionParser._eval_node(node.right, context)
            op = SafeASTExpressionParser.OPERATORS.get(type(node.op))
            if not op:
                raise TypeError(f"Unsupported binary operator: {type(node.op)}")
            return op(left, right)
        elif isinstance(node, ast.Compare):
            left = SafeASTExpressionParser._eval_node(node.left, context)
            for op_node, comparator in zip(node.ops, node.comparators):
                right = SafeASTExpressionParser._eval_node(comparator, context)
                op = SafeASTExpressionParser.OPERATORS.get(type(op_node))
                if not op or not op(left, right):
                    return False
                left = right
            return True
        elif isinstance(node, ast.UnaryOp):
            operand = SafeASTExpressionParser._eval_node(node.operand, context)
            op = SafeASTExpressionParser.OPERATORS.get(type(node.op))
            return op(operand)
        raise ValueError(f"Disallowed AST node type in sandbox: {type(node)}")
""")

    # 3. backend/app/enterprise/domain_handlers/commission_split_calculator.py
    write_file("backend/app/enterprise/domain_handlers/commission_split_calculator.py", """from typing import Any, Dict, List, Optional

class CommissionSplitCalculator:
    @staticmethod
    def calculate_deal_splits(
        deal_value: float,
        split_allocations: List[Dict[str, Any]], # rep_id, percentage, role
        base_rate: float = 0.10
    ) -> Dict[str, Any]:
        total_pct = sum(float(s.get("percentage", 0.0)) for s in split_allocations)
        if total_pct != 100.0:
            raise ValueError(f"Split percentages must sum to exactly 100.0% (current: {total_pct}%).")

        splits = []
        total_commission_pool = deal_value * base_rate

        for s in split_allocations:
            pct = float(s.get("percentage", 0.0))
            rep_id = s.get("rep_id")
            role = s.get("role", "Sales Rep")
            allocated_deal_value = round(deal_value * (pct / 100.0), 2)
            commission_payout = round(total_commission_pool * (pct / 100.0), 2)

            splits.append({
                "rep_id": rep_id,
                "role": role,
                "split_percentage": pct,
                "credited_deal_value": allocated_deal_value,
                "commission_payout": commission_payout
            })

        return {
            "deal_value": deal_value,
            "total_commission_pool": round(total_commission_pool, 2),
            "splits": splits
        }
""")

    # 4. frontend/src/enterprise/EnterpriseMarketingAttributionMatrix.tsx
    write_file("frontend/src/enterprise/EnterpriseMarketingAttributionMatrix.tsx", """import React, { useState } from "react";
import { Award, TrendingUp, Filter, ArrowUpRight, DollarSign } from "lucide-react";

export const EnterpriseMarketingAttributionMatrix: React.FC = () => {
  const channels = [
    { channel: "Direct Executive Outreach", cost: 15000, revenue: 320000, roas: "21.3x", leads: 42, wonDeals: 12 },
    { channel: "Google Search (High-Intent B2B)", cost: 25000, revenue: 410000, roas: "16.4x", leads: 180, wonDeals: 18 },
    { channel: "LinkedIn Sponsored Content", cost: 18000, revenue: 195000, roas: "10.8x", leads: 95, wonDeals: 8 },
    { channel: "Product Demonstration Webinars", cost: 8000, revenue: 160000, roas: "20.0x", leads: 64, wonDeals: 7 }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-emerald-400" />
            Marketing Campaign ROI & Multi-Channel Performance
          </h3>
          <p className="text-xs text-slate-400">Return on Ad Spend (ROAS) and direct pipeline conversion attribution across marketing channels</p>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-xs text-left">
          <thead className="bg-slate-950 text-slate-400 font-semibold border-b border-slate-800">
            <tr>
              <th className="p-3">Campaign Channel</th>
              <th className="p-3 text-right">Spend</th>
              <th className="p-3 text-right">Leads</th>
              <th className="p-3 text-right">Won Deals</th>
              <th className="p-3 text-right text-emerald-400">Revenue Attributed</th>
              <th className="p-3 text-right">ROAS</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-white">
            {channels.map((ch, idx) => (
              <tr key={idx} className="hover:bg-slate-800/30">
                <td className="p-3 font-medium">{ch.channel}</td>
                <td className="p-3 text-right text-slate-400">${ch.cost.toLocaleString()}</td>
                <td className="p-3 text-right">{ch.leads}</td>
                <td className="p-3 text-right">{ch.wonDeals}</td>
                <td className="p-3 text-right font-bold text-emerald-400">${ch.revenue.toLocaleString()}</td>
                <td className="p-3 text-right font-bold text-purple-400">{ch.roas}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
""")

    print("Created event stream processor, AST parser, commission splits, and marketing matrix UI.")

if __name__ == '__main__':
    run()
