"""
Automated database seeder for portfolio demonstration.
Creates demo user, demo project, benchmark dataset, and sample MLflow experiment.
"""
import sys
import os

# Add backend directory to sys.path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
sys.path.insert(0, backend_path)

try:
    from app.database.session import SessionLocal
    from app.models.user import User
    from app.models.project import Project
    from app.models.dataset import Dataset
    from app.core.security import get_password_hash
    from scripts.generate_benchmark_data import generate_datasets
except ImportError as e:
    print(f"Error importing backend modules: {e}")
    sys.exit(1)

def seed_database():
    db = SessionLocal()
    try:
        # 1. Create Demo User
        demo_email = "demo@orchestrator.ai"
        user = db.query(User).filter(User.email == demo_email).first()
        if not user:
            user = User(
                email=demo_email,
                hashed_password=get_password_hash("demo1234"),
                full_name="Demo Researcher"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"Created demo user: {demo_email} (password: demo1234)")
        else:
            print(f"Demo user already exists: {demo_email}")

        # 2. Create Demo Project
        project = db.query(Project).filter(Project.name == "Telco Churn Production Benchmark", Project.owner_id == user.id).first()
        if not project:
            project = Project(
                name="Telco Churn Production Benchmark",
                description="Production benchmark evaluating XGBoost and LightGBM models for proactive customer retention.",
                owner_id=user.id
            )
            db.add(project)
            db.commit()
            db.refresh(project)
            print(f"Created demo project: {project.name}")
        else:
            print(f"Demo project already exists: {project.name}")

        # 3. Ensure Benchmark CSV exists
        generate_datasets()
        csv_file = os.path.abspath("demo_data/customer_churn_benchmark.csv")

        # 4. Link Dataset in DB
        ds = db.query(Dataset).filter(Dataset.name == "customer_churn_benchmark.csv", Dataset.project_id == project.id).first()
        if not ds:
            ds = Dataset(
                name="customer_churn_benchmark.csv",
                description="Synthetic telco customer churn dataset with tenure, charges, and support tickets.",
                file_path=csv_file,
                file_size=os.path.getsize(csv_file),
                project_id=project.id
            )
            db.add(ds)
            db.commit()
            print("Linked demo dataset to project.")

        print("\n✅ SEEDING COMPLETE! You can log in using:")
        print(f"   Email:    {demo_email}")
        print("   Password: demo1234")

    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
