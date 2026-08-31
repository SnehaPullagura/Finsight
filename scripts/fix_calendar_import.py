import os
import sys

with open("backend/app/api/v1/endpoints/calendar.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("from typing import List", "from typing import List, Optional")

with open("backend/app/api/v1/endpoints/calendar.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Fixed calendar.py import.")
