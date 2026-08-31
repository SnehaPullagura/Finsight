from fastapi import APIRouter
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
