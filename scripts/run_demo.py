"""
One-click CLI utility to seed and launch the ML Experiment Orchestrator demo.
"""
import os
import sys
import subprocess

def main():
    print("=" * 65)
    print("🚀 ML Experiment Orchestrator — Demo Environment Launcher")
    print("=" * 65)

    # 1. Run seed script
    print("\n[1/2] Seeding benchmark datasets and demo user...")
    subprocess.run([sys.executable, "scripts/seed_demo_data.py"], check=True)

    print("\n[2/2] Setup complete!")
    print("-" * 65)
    print("To launch the platform:")
    print("  Backend:   uvicorn app.main:app --reload (inside backend/)")
    print("  Frontend:  streamlit run app.py (inside frontend/)")
    print("  Docker:    docker-compose up --build")
    print("-" * 65)
    print("Default Demo Credentials:")
    print("  Email:    demo@orchestrator.ai")
    print("  Password: demo1234")
    print("=" * 65)

if __name__ == "__main__":
    main()
