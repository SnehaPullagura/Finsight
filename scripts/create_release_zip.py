import os
import zipfile
import sys

def create_zip():
    output_filename = "clientflowCRM_release.zip"
    ignore_dirs = {".git", "node_modules", ".pytest_cache", "__pycache__", ".ruff_cache", "venv", ".venv"}
    ignore_files = {output_filename, ".DS_Store"}

    print(f"Creating archive '{output_filename}'...")
    total_files = 0

    with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk("."):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            # Skip top-level ignore dirs
            rel_root = os.path.relpath(root, ".")
            top_dir = rel_root.split(os.sep)[0] if rel_root != "." else ""
            if top_dir in ignore_dirs:
                continue

            for f in files:
                if f in ignore_files or f.endswith(".pyc"):
                    continue

                filepath = os.path.join(root, f)
                arcname = os.path.relpath(filepath, ".")
                zipf.write(filepath, arcname)
                total_files += 1

    size_mb = os.path.getsize(output_filename) / (1024 * 1024)
    print("=" * 60)
    print(f"Archive Created Successfully: {os.path.abspath(output_filename)}")
    print(f"Total Files Packaged: {total_files}")
    print(f"Archive Size: {size_mb:.2f} MB")
    print("=" * 60)

if __name__ == '__main__':
    create_zip()
