import sys
import os

with open("pyproject.toml", "w", encoding="utf-8") as f:
    f.write("""[tool.pytest.ini_options]
minversion = "8.0"
addopts = "-ra -q --asyncio-mode=auto"
testpaths = ["tests"]
pythonpath = ["."]
python_files = ["test_*.py"]
filterwarnings = [
    "ignore::DeprecationWarning",
    "ignore::UserWarning",
]
""")

with open("tests/conftest.py", "r", encoding="utf-8") as f:
    content = f.read()

if "sys.path.insert" not in content:
    content = """import sys
import os
sys.path.insert(0, os.path.abspath("."))
""" + content

with open("tests/conftest.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated root pyproject.toml and tests/conftest.py")
