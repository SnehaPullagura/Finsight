import os
import sys
sys.path.insert(0, os.path.abspath("."))

def run():
    # 1. endpoints/cpq.py
    with open("backend/app/api/v1/endpoints/cpq.py", "r", encoding="utf-8") as f:
        c = f.read()
    c = c.replace("from backend.app.schemas.cpq import", "from backend.app.cpq.schemas import")
    with open("backend/app/api/v1/endpoints/cpq.py", "w", encoding="utf-8") as f:
        f.write(c)

    # 2. endpoints/billing.py
    with open("backend/app/api/v1/endpoints/billing.py", "r", encoding="utf-8") as f:
        c = f.read()
    c = c.replace("from backend.app.schemas.billing import", "from backend.app.billing.schemas import")
    with open("backend/app/api/v1/endpoints/billing.py", "w", encoding="utf-8") as f:
        f.write(c)

    # 3. endpoints/advanced_analytics.py
    with open("backend/app/api/v1/endpoints/advanced_analytics.py", "r", encoding="utf-8") as f:
        c = f.read()
    c = c.replace("from backend.app.schemas.analytics import", "from backend.app.analytics.schemas import")
    with open("backend/app/api/v1/endpoints/advanced_analytics.py", "w", encoding="utf-8") as f:
        f.write(c)

    # 4. endpoints/integrations_hub.py
    with open("backend/app/api/v1/endpoints/integrations_hub.py", "r", encoding="utf-8") as f:
        c = f.read()
    c = c.replace("from backend.app.schemas.integrations import", "from backend.app.integrations.schemas import")
    with open("backend/app/api/v1/endpoints/integrations_hub.py", "w", encoding="utf-8") as f:
        f.write(c)

    print("Fixed endpoint schema imports.")

if __name__ == '__main__':
    run()
