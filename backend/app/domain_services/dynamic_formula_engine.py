import math
import re
from datetime import datetime, date
from typing import Any, Dict, List, Optional, Union

class DynamicFormulaEngine:
    FUNCTIONS = {
        "UPPER": lambda val: str(val).upper() if val is not None else "",
        "LOWER": lambda val: str(val).lower() if val is not None else "",
        "CONCAT": lambda *args: "".join(str(a) for a in args if a is not None),
        "ROUND": lambda num, decimals=2: round(float(num), int(decimals)),
        "ABS": lambda num: abs(float(num)),
        "MAX": lambda *args: max(float(a) for a in args),
        "MIN": lambda *args: min(float(a) for a in args),
        "IF": lambda cond, true_val, false_val: true_val if cond else false_val,
        "NOW": lambda: datetime.utcnow().isoformat(),
        "TODAY": lambda: date.today().isoformat()
    }

    @staticmethod
    def evaluate_formula(formula_str: str, context: Dict[str, Any]) -> Any:
        expression = formula_str.strip()
        
        # Replace context variables enclosed in braces e.g. {deal.value} * {deal.tax_rate}
        def replace_var(match):
            var_name = match.group(1).strip()
            # Support dotted navigation e.g. company.revenue
            parts = var_name.split(".")
            curr = context
            for p in parts:
                if isinstance(curr, dict) and p in curr:
                    curr = curr[p]
                else:
                    return "0"
            return str(curr)

        parsed_expr = re.sub(r"\{([a-zA-Z0-9_\.]+)\}", replace_var, expression)
        
        try:
            # Safe evaluation with restricted globals
            from backend.app.workflow.ast_evaluator import SafeExpressionEvaluator
            return SafeExpressionEvaluator.evaluate(parsed_expr, context)
        except Exception:
            return parsed_expr
