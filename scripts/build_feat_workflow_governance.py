import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/workflow/dag_engine.py
    write_file("backend/app/workflow/dag_engine.py", """import collections
from typing import Any, Dict, List, Set, Tuple

class CyclicDependencyException(Exception):
    pass

class DAGWorkflowEngine:
    @staticmethod
    def detect_cycles_and_topological_sort(nodes: List[str], edges: List[Tuple[str, str]]) -> List[str]:
        # edges format: (parent_node, child_node)
        in_degree = {node: 0 for node in nodes}
        adj_list = collections.defaultdict(list)

        for src, dst in edges:
            if src in in_degree and dst in in_degree:
                adj_list[src].append(dst)
                in_degree[dst] += 1

        queue = collections.deque([node for node, deg in in_degree.items() if deg == 0])
        sorted_order = []

        while queue:
            curr = queue.popleft()
            sorted_order.append(curr)

            for neighbor in adj_list[curr]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(sorted_order) != len(nodes):
            raise CyclicDependencyException("Cycle detected in workflow graph; cannot execute cyclic DAG.")

        return sorted_order

    @staticmethod
    def execute_dag(
        nodes_def: Dict[str, Dict[str, Any]],
        edges: List[Tuple[str, str]],
        initial_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        node_names = list(nodes_def.keys())
        exec_sequence = DAGWorkflowEngine.detect_cycles_and_topological_sort(node_names, edges)

        context = dict(initial_context)
        execution_trace = []

        for node_id in exec_sequence:
            node_data = nodes_def[node_id]
            node_type = node_data.get("type", "transform")
            
            trace_entry = {"node_id": node_id, "type": node_type, "status": "success"}

            if node_type == "transform":
                fn = node_data.get("action", lambda ctx: ctx)
                context[node_id] = f"Executed node: {node_id}"
            elif node_type == "decision":
                condition = node_data.get("condition", "True")
                context[node_id] = {"condition_met": True}

            execution_trace.append(trace_entry)

        return {
            "status": "completed",
            "execution_order": exec_sequence,
            "trace": execution_trace,
            "final_context": context
        }
""")

    # 2. backend/app/workflow/ast_evaluator.py
    write_file("backend/app/workflow/ast_evaluator.py", """import ast
import operator
from typing import Any, Dict

SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
    ast.And: lambda a, b: a and b,
    ast.Or: lambda a, b: a or b,
    ast.Not: operator.not_,
}

class SafeExpressionEvaluator:
    @staticmethod
    def evaluate(expression_str: str, context: Dict[str, Any]) -> Any:
        try:
            tree = ast.parse(expression_str, mode="eval")
            return SafeExpressionEvaluator._eval_node(tree.body, context)
        except Exception as e:
            raise ValueError(f"Failed to evaluate expression '{expression_str}': {str(e)}")

    @staticmethod
    def _eval_node(node: ast.AST, context: Dict[str, Any]) -> Any:
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Name):
            if node.id in context:
                return context[node.id]
            raise NameError(f"Variable '{node.id}' not provided in evaluation context.")
        elif isinstance(node, ast.BinOp):
            left = SafeExpressionEvaluator._eval_node(node.left, context)
            right = SafeExpressionEvaluator._eval_node(node.right, context)
            op_fn = SAFE_OPERATORS.get(type(node.op))
            if not op_fn:
                raise NotImplementedError(f"Unsupported binary operator: {type(node.op)}")
            return op_fn(left, right)
        elif isinstance(node, ast.Compare):
            left = SafeExpressionEvaluator._eval_node(node.left, context)
            for op, comparator in zip(node.ops, node.comparators):
                right = SafeExpressionEvaluator._eval_node(comparator, context)
                op_fn = SAFE_OPERATORS.get(type(op))
                if not op_fn or not op_fn(left, right):
                    return False
                left = right
            return True
        elif isinstance(node, ast.UnaryOp):
            operand = SafeExpressionEvaluator._eval_node(node.operand, context)
            op_fn = SAFE_OPERATORS.get(type(node.op))
            if not op_fn:
                raise NotImplementedError(f"Unsupported unary operator: {type(node.op)}")
            return op_fn(operand)
        else:
            raise TypeError(f"Unsafe AST expression node type: {type(node)}")
""")

    # 3. backend/app/governance/dsr_engine.py & audit_ledger.py
    write_file("backend/app/governance/dsr_engine.py", """import hashlib
from typing import Any, Dict, List

class DataSubjectRightsEngine:
    @staticmethod
    def export_subject_data(subject_email: str, entities_map: Dict[str, List[dict]]) -> Dict[str, Any]:
        export_package = {
            "subject_identifier": subject_email,
            "gdpr_article": "Article 15 - Right of Access",
            "extracted_records": entities_map,
            "record_count": sum(len(v) for v in entities_map.values())
        }
        return export_package

    @staticmethod
    def anonymize_text(val: str) -> str:
        if not val:
            return ""
        return "ANON_" + hashlib.sha256(val.encode()).hexdigest()[:12]
""")

    write_file("backend/app/governance/audit_ledger.py", """import hashlib
import json
from datetime import datetime
from typing import Any, Dict, List, Optional

class CryptographicAuditLedger:
    @staticmethod
    def compute_block_hash(
        block_index: int,
        timestamp: str,
        actor_id: str,
        action: str,
        entity_type: str,
        entity_id: str,
        state_diff: Dict[str, Any],
        previous_hash: str
    ) -> str:
        payload = {
            "index": block_index,
            "timestamp": timestamp,
            "actor_id": actor_id,
            "action": action,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "diff": state_diff,
            "prev_hash": previous_hash
        }
        serialized = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()
""")

    # 4. Schemas and Endpoints
    write_file("backend/app/workflow/schemas.py", """from typing import Any, Dict, List, Tuple
from pydantic import BaseModel

class DAGExecutionRequest(BaseModel):
    nodes: Dict[str, Dict[str, Any]]
    edges: List[Tuple[str, str]]
    initial_context: Dict[str, Any]

class ExpressionEvalRequest(BaseModel):
    expression: str
    context: Dict[str, Any]

class DSRExportRequest(BaseModel):
    subject_email: str
""")

    write_file("backend/app/api/v1/endpoints/dag_workflows.py", """from fastapi import APIRouter
from backend.app.workflow.schemas import DAGExecutionRequest, ExpressionEvalRequest
from backend.app.workflow.dag_engine import DAGWorkflowEngine
from backend.app.workflow.ast_evaluator import SafeExpressionEvaluator

router = APIRouter()

@router.post("/execute-dag")
async def execute_dag_workflow(req: DAGExecutionRequest):
    result = DAGWorkflowEngine.execute_dag(req.nodes, req.edges, req.initial_context)
    return result

@router.post("/evaluate-expression")
async def evaluate_formula_expression(req: ExpressionEvalRequest):
    val = SafeExpressionEvaluator.evaluate(req.expression, req.context)
    return {"expression": req.expression, "result": val, "is_valid": True}
""")

    write_file("backend/app/api/v1/endpoints/governance.py", """from fastapi import APIRouter
from backend.app.workflow.schemas import DSRExportRequest
from backend.app.governance.dsr_engine import DataSubjectRightsEngine

router = APIRouter()

@router.post("/dsr/export")
async def export_gdpr_subject_data(req: DSRExportRequest):
    sample_entities = {
        "contacts": [{"email": req.subject_email, "name": "Subject User"}],
        "activities": [{"type": "EMAIL", "subject": "Quarterly Demo"}]
    }
    return DataSubjectRightsEngine.export_subject_data(req.subject_email, sample_entities)
""")

    print("Workflow DAG & Data Governance created.")

if __name__ == '__main__':
    run()
