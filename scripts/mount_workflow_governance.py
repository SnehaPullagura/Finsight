with open("backend/app/api/v1/api.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("integrations_hub", "integrations_hub, dag_workflows, governance")
content = content.replace(
    """api_router.include_router(integrations_hub.router, prefix="/integrations-hub", tags=["Integrations Hub & Migration"])""",
    """api_router.include_router(integrations_hub.router, prefix="/integrations-hub", tags=["Integrations Hub & Migration"])
api_router.include_router(dag_workflows.router, prefix="/dag-workflows", tags=["DAG Workflow Engine"])
api_router.include_router(governance.router, prefix="/governance", tags=["Data Governance & Compliance"])"""
)

with open("backend/app/api/v1/api.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Mounted dag_workflows and governance routers.")
