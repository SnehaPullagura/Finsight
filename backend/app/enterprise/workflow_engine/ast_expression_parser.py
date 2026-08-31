import ast
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
