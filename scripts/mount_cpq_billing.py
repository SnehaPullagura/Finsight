with open("backend/app/api/v1/api.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("campaigns, automations, search, analytics", "campaigns, automations, search, analytics, cpq, billing")
content = content.replace(
    """api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics & Dashboard"])""",
    """api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics & Dashboard"])
api_router.include_router(cpq.router, prefix="/cpq", tags=["CPQ & Pricing Engine"])
api_router.include_router(billing.router, prefix="/billing", tags=["Subscription Billing"])"""
)

with open("backend/app/api/v1/api.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Mounted CPQ and Billing routers.")
