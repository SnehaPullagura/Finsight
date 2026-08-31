import os
import json

# 1. Update LICENSE
with open("LICENSE", "w", encoding="utf-8") as f:
    f.write("""PROPRIETARY AND CONFIDENTIAL

Copyright (c) 2026 ClientFlow CRM. All Rights Reserved.

This software and its documentation are proprietary to ClientFlow CRM.
Unauthorized copying, modification, distribution, transmission, or reproduction
of this software, via any medium, is strictly prohibited.
""")

# 2. Update frontend/package.json
with open("frontend/package.json", "r", encoding="utf-8") as f:
    pkg = json.load(f)
pkg["license"] = "UNLICENSED"
pkg["private"] = True
with open("frontend/package.json", "w", encoding="utf-8") as f:
    json.dump(pkg, f, indent=2)

# 3. Update .gitignore
with open(".gitignore", "r", encoding="utf-8") as f:
    gi = f.read()

if ".env" not in gi:
    gi += "\n.env\n.env.*\n*.db\n*.sqlite3\n*.zip\n"
else:
    gi = gi.replace(".env.example", "") # ensure ignored
    if ".env*" not in gi:
        gi += "\n.env*\n*.zip\n"

with open(".gitignore", "w", encoding="utf-8") as f:
    f.write(gi)

print("Updated LICENSE to Proprietary, set UNLICENSED in package.json, and updated .gitignore.")
