with open("backend/app/api/v1/api.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("cpq, billing", "cpq, billing, advanced_analytics")
content = content.replace(
    """api_router.include_router(billing.router, prefix="/billing", tags=["Subscription Billing"])""",
    """api_router.include_router(billing.router, prefix="/billing", tags=["Subscription Billing"])
api_router.include_router(advanced_analytics.router, prefix="/advanced-analytics", tags=["Advanced Analytics & Forecasting"])"""
)

with open("backend/app/api/v1/api.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Mounted advanced_analytics router.")
