with open("backend/app/api/v1/api.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("cpq, billing, advanced_analytics", "cpq, billing, advanced_analytics, integrations_hub")
content = content.replace(
    """api_router.include_router(advanced_analytics.router, prefix="/advanced-analytics", tags=["Advanced Analytics & Forecasting"])""",
    """api_router.include_router(advanced_analytics.router, prefix="/advanced-analytics", tags=["Advanced Analytics & Forecasting"])
api_router.include_router(integrations_hub.router, prefix="/integrations-hub", tags=["Integrations Hub & Migration"])"""
)

with open("backend/app/api/v1/api.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Mounted integrations_hub router.")
