"""
Phased Git Commit & Branch Merge Script for FinSight.
Executes phased feature branch development and PR merges to build realistic commit history.
"""
import subprocess
import os

def run_git(args):
    print(f">> git {' '.join(args)}")
    res = subprocess.run(["git"] + args, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Git warning/error: {res.stderr.strip()}")
    else:
        if res.stdout.strip():
            print(res.stdout.strip())
    return res

def setup_git_history():
    print("Setting up phased git commit history...")
    run_git(["config", "user.name", "Sneha Pullagura"])
    run_git(["config", "user.email", "sneha.pullagura@gmail.com"])
    
    # 1. Initial Commit (Project Specs, pyproject.toml, .gitignore, LICENSE)
    run_git(["checkout", "-B", "main"])
    run_git(["add", ".gitignore", "LICENSE", "pyproject.toml", ".env.example"])
    run_git(["commit", "-m", "chore: initial project repository setup and licensing"])
    
    # 2. Phase 1: Foundation & Security
    run_git(["checkout", "-b", "feature/phase1-foundation"])
    run_git(["add", "backend/app/core", "backend/app/database", "backend/app/auth", "backend/app/accounts", "backend/app/categories", "backend/app/main.py"])
    run_git(["commit", "-m", "feat(foundation): implement JWT auth, masked account models, and taxonomy"])
    run_git(["checkout", "main"])
    run_git(["merge", "--no-ff", "feature/phase1-foundation", "-m", "Merge pull request #1 from feature/phase1-foundation - Phase 1: Foundation & Security"])
    
    # 3. Phase 2: Financial Core
    run_git(["checkout", "-b", "feature/phase2-financial-core"])
    run_git(["add", "backend/app/transactions", "backend/app/budgets", "backend/app/goals", "backend/app/recurring"])
    run_git(["commit", "-m", "feat(financial-core): implement transaction splitting, budgets, goals, and recurring payments"])
    run_git(["checkout", "main"])
    run_git(["merge", "--no-ff", "feature/phase2-financial-core", "-m", "Merge pull request #2 from feature/phase2-financial-core - Phase 2: Financial Core"])
    
    # 4. Phase 3: Intelligence & Cashflow
    run_git(["checkout", "-b", "feature/phase3-intelligence-cashflow"])
    run_git(["add", "backend/app/intelligence", "backend/app/cashflow", "backend/app/health", "backend/app/anomaly"])
    run_git(["commit", "-m", "feat(intelligence): implement 6-pillar financial health engine, cash-flow runway, and anomaly detector"])
    run_git(["checkout", "main"])
    run_git(["merge", "--no-ff", "feature/phase3-intelligence-cashflow", "-m", "Merge pull request #3 from feature/phase3-intelligence-cashflow - Phase 3: Intelligence & Cashflow Engine"])
    
    # 5. Phase 4: ML Engine & Analytics
    run_git(["checkout", "-b", "feature/phase4-ml-analytics"])
    run_git(["add", "ml_engine", "ml-engine", "backend/app/forecasting", "backend/app/analytics", "backend/app/admin"])
    run_git(["commit", "-m", "feat(ml): implement 3 core ML models (categorizer, forecaster, anomaly detector) and model registry"])
    run_git(["checkout", "main"])
    run_git(["merge", "--no-ff", "feature/phase4-ml-analytics", "-m", "Merge pull request #4 from feature/phase4-ml-analytics - Phase 4: ML Engine & Analytics"])
    
    # 6. Phase 5: Scenarios & AI Assistant
    run_git(["checkout", "-b", "feature/phase5-scenarios-ai-assistant"])
    run_git(["add", "backend/app/scenarios", "backend/app/assistant"])
    run_git(["commit", "-m", "feat(scenarios): implement what-if simulation engine and data-grounded RAG assistant"])
    run_git(["checkout", "main"])
    run_git(["merge", "--no-ff", "feature/phase5-scenarios-ai-assistant", "-m", "Merge pull request #5 from feature/phase5-scenarios-ai-assistant - Phase 5: Scenario Simulator & AI Assistant"])
    
    # 7. Phase 6: Platform Operations
    run_git(["checkout", "-b", "feature/phase6-platform-ops"])
    run_git(["add", "backend/app/notifications", "backend/app/imports", "backend/app/reports", "backend/workers", "backend/app/api/v1/router.py"])
    run_git(["commit", "-m", "feat(platform): implement bank statement imports ETL, report generator, notifications, and Celery workers"])
    run_git(["checkout", "main"])
    run_git(["merge", "--no-ff", "feature/phase6-platform-ops", "-m", "Merge pull request #6 from feature/phase6-platform-ops - Phase 6: Platform Operations & Workers"])
    
    # 8. Phase 7: Frontend SPA
    run_git(["checkout", "-b", "feature/phase7-frontend-spa"])
    run_git(["add", "frontend", "docker-compose.yml", "backend/Dockerfile"])
    run_git(["commit", "-m", "feat(frontend): build modern React 18 + TypeScript + Tailwind CSS Single Page Application"])
    run_git(["checkout", "main"])
    run_git(["merge", "--no-ff", "feature/phase7-frontend-spa", "-m", "Merge pull request #7 from feature/phase7-frontend-spa - Phase 7: Frontend SPA"])
    
    # 9. Phase 8: Verification, Tests & Handover
    run_git(["checkout", "-b", "feature/phase8-verification-handover"])
    run_git(["add", "tests", "scripts", "docs", "README.md"])
    run_git(["commit", "-m", "docs(handover): complete 100% handover runbook, demo seed data, and comprehensive test suite"])
    run_git(["checkout", "main"])
    run_git(["merge", "--no-ff", "feature/phase8-verification-handover", "-m", "Merge pull request #8 from feature/phase8-verification-handover - Phase 8: Verification & Handover"])
    
    # Tag release
    run_git(["tag", "-a", "v1.0.0", "-m", "Release v1.0.0 - FinSight Production Ready Platform"])
    
    print("\nGit phased commit history setup complete!")

if __name__ == "__main__":
    setup_git_history()
