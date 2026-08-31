import os
import sys
import importlib
sys.path.insert(0, os.path.abspath("."))

failed = []
for root, dirs, files in os.walk("backend/app"):
    for f in files:
        if f.endswith(".py") and not f.startswith("__"):
            rel_path = os.path.relpath(os.path.join(root, f), ".")
            mod_name = rel_path.replace(os.sep, ".").replace(".py", "")
            try:
                importlib.import_module(mod_name)
                print(f"OK: {mod_name}")
            except Exception as e:
                print(f"ERROR: {mod_name} -> {e}")
                failed.append((mod_name, str(e)))

print("Total modules checked. Failures:", len(failed))
