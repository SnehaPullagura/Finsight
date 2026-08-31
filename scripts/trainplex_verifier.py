"""
TrainPlex Checker Automated Verification & Submission Script
Packages the repository (including .git) into a zip file, submits to the TrainPlex Checker Bot,
and verifies 100% compliance across all 14 criteria.
"""
import os
import sys
import zipfile
import requests
import json

CHECKER_API_URL = "https://train-plex-checker-bot-1--ttejaswar1234.replit.app/api/check"
ZIP_OUTPUT = "finsight_submission.zip"
EXCLUDE_DIRS = {".venv", "venv", "node_modules", ".pytest_cache", "__pycache__", "dist", ".tox"}

def create_submission_zip(output_filename=ZIP_OUTPUT):
    print(f"Packaging codebase into '{output_filename}'...")
    root_dir = os.path.abspath(".")
    count = 0
    
    with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            
            for file in files:
                if file == output_filename or file.endswith(".pyc"):
                    continue
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, root_dir)
                zipf.write(file_path, arcname)
                count += 1
                
    size_mb = os.path.getsize(output_filename) / (1024 * 1024)
    print(f"Created '{output_filename}' with {count} files ({size_mb:.2f} MB)")
    return output_filename

def submit_to_checker(zip_path=ZIP_OUTPUT):
    print(f"Submitting '{zip_path}' to TrainPlex Checker ({CHECKER_API_URL})...")
    
    with open(zip_path, "rb") as f:
        files = {"file": (os.path.basename(zip_path), f, "application/zip")}
        try:
            response = requests.post(CHECKER_API_URL, files=files, timeout=120)
            print(f"Response Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                tp = data.get("trainplex", {})
                summary = tp.get("summary", {})
                checks = tp.get("checks", [])
                
                print("\n" + "="*70)
                print("TRAINPLEX CHECKER AUDIT RESULT (14-POINT VERIFICATION)")
                print("="*70)
                print(f"Passed Checks    : {summary.get('passed', 0)} / {summary.get('total', 14)}")
                print(f"Failed Checks    : {summary.get('failed', 0)}")
                print(f"Warnings         : {summary.get('warnings', 0)}")
                print(f"Readiness Score  : {summary.get('score_pct', 0)}%")
                print(f"Ready for Review : {summary.get('ready', False)}")
                print("-"*70)
                
                for idx, c in enumerate(checks, 1):
                    status_symbol = "[PASS]" if c.get("status") == "pass" else "[FAIL]"
                    print(f"{idx:2d}. {status_symbol} {c.get('name')}")
                    print(f"    Category : {c.get('category')}")
                    print(f"    Details  : {c.get('details')}")
                    print(f"    Fix      : {c.get('fix')}")
                    print()
                        
                print("="*70 + "\n")
                return data
            else:
                print(f"Error from checker: {response.text}")
                return None
        except Exception as e:
            print(f"Submission failed: {e}")
            return None

if __name__ == "__main__":
    zip_file = create_submission_zip()
    submit_to_checker(zip_file)
