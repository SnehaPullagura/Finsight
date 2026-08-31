import ast
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
