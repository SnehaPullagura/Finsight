import os
import sys
sys.path.insert(0, os.path.abspath("."))

with open("backend/app/services/lead.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("from typing import Dict, List, Optional, Tuple", "from typing import Any, Dict, List, Optional, Tuple")

with open("backend/app/services/lead.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Fixed lead.py imports.")
