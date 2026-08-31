import os
from collections import defaultdict

EXTENSIONS = {
    ".py": "Python",
    ".ts": "TypeScript",
    ".tsx": "TypeScript React",
    ".js": "JavaScript",
    ".jsx": "JavaScript React",
    ".css": "CSS",
    ".html": "HTML",
    ".json": "JSON",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".md": "Markdown",
    ".sql": "SQL",
    ".toml": "TOML",
    ".sh": "Shell",
    ".dockerfile": "Dockerfile",
}

IGNORE_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build", ".pytest_cache", ".ruff_cache"}

def count_loc():
    stats = defaultdict(lambda: {"files": 0, "lines": 0, "blank": 0, "comment": 0, "code": 0})
    dir_stats = defaultdict(lambda: {"files": 0, "lines": 0, "code": 0})

    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        rel_root = os.path.relpath(root, ".")
        top_dir = rel_root.split(os.sep)[0] if rel_root != "." else "root"
        if top_dir in IGNORE_DIRS:
            continue

        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if f.lower() in ["dockerfile", "dockerfile.backend", "dockerfile.frontend", "dockerfile.worker"]:
                ext = ".dockerfile"
            
            if ext in EXTENSIONS:
                lang = EXTENSIONS[ext]
                filepath = os.path.join(root, f)
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as fp:
                        lines = fp.readlines()
                        total_l = len(lines)
                        blank_l = sum(1 for line in lines if not line.strip())
                        code_l = total_l - blank_l

                        stats[lang]["files"] += 1
                        stats[lang]["lines"] += total_l
                        stats[lang]["blank"] += blank_l
                        stats[lang]["code"] += code_l

                        dir_stats[top_dir]["files"] += 1
                        dir_stats[top_dir]["lines"] += total_l
                        dir_stats[top_dir]["code"] += code_l
                except Exception:
                    pass

    print("=" * 70)
    print("           CLIENTFLOW CRM — SOURCE CODE & METRICS REPORT           ")
    print("=" * 70)
    print(f"{'Language':<20} | {'Files':<8} | {'Total Lines':<12} | {'Code Lines':<10}")
    print("-" * 70)
    
    grand_files = 0
    grand_lines = 0
    grand_code = 0

    for lang, data in sorted(stats.items(), key=lambda x: x[1]["code"], reverse=True):
        print(f"{lang:<20} | {data['files']:<8} | {data['lines']:<12} | {data['code']:<10}")
        grand_files += data["files"]
        grand_lines += data["lines"]
        grand_code += data["code"]

    print("-" * 70)
    print(f"{'TOTAL':<20} | {grand_files:<8} | {grand_lines:<12} | {grand_code:<10}")
    print("=" * 70)
    print("\nDIRECTORY BREAKDOWN:")
    print("-" * 70)
    print(f"{'Directory':<20} | {'Files':<8} | {'Total Lines':<12} | {'Code Lines':<10}")
    print("-" * 70)
    for d, data in sorted(dir_stats.items(), key=lambda x: x[1]["code"], reverse=True):
        print(f"{d:<20} | {data['files']:<8} | {data['lines']:<12} | {data['code']:<10}")
    print("=" * 70)

if __name__ == '__main__':
    count_loc()
