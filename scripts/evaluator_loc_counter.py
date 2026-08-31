import os
import sys

def count_evaluator_prod_loc():
    total_loc = 0
    file_count = 0
    by_lang = {"Python": 0, "TypeScript": 0, "JavaScript": 0}

    scan_dirs = ["backend", os.path.join("frontend", "src")]

    for scan_dir in scan_dirs:
        for root, dirs, files in os.walk(scan_dir):
            if any(p in root for p in ["tests", "node_modules", ".git", "coverage", "dist", "__pycache__", ".pytest_cache"]):
                continue
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                lang = None
                if ext == ".py":
                    lang = "Python"
                elif ext in [".ts", ".tsx"]:
                    lang = "TypeScript"
                elif ext == ".js":
                    lang = "JavaScript"

                if lang:
                    fpath = os.path.join(root, f)
                    try:
                        with open(fpath, "r", encoding="utf-8", errors="ignore") as fh:
                            lines = len(fh.readlines())
                            total_loc += lines
                            file_count += 1
                            by_lang[lang] += lines
                    except Exception:
                        pass

    print(f"Evaluator Prod LOC: {total_loc:,} across {file_count} files.")
    for l, c in by_lang.items():
        print(f"  {l}: {c:,}")
    return total_loc

if __name__ == "__main__":
    count_evaluator_prod_loc()
