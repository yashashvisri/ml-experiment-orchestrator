"""
Generates synthetic benchmark datasets for immediate testing and demonstration.
"""
import os
import pandas as pd
import numpy as np

def generate_datasets():
    os.makedirs("demo_data", exist_ok=True)
    np.random.seed(42)

    # 1. Customer Churn Benchmark
    n = 1000
    tenure = np.random.randint(1, 72, size=n)
    monthly_charges = np.round(np.random.uniform(20.0, 118.0, size=n), 2)
    total_charges = np.round(tenure * monthly_charges * np.random.uniform(0.9, 1.1, size=n), 2)
    contract = np.random.choice(["Month-to-month", "One year", "Two year"], size=n, p=[0.55, 0.25, 0.20])
    support_tickets = np.random.poisson(lam=1.5, size=n)
    
    # Target probability influenced by contract & monthly charges
    prob = 0.2 + (monthly_charges / 300.0) - (tenure / 150.0) + (support_tickets * 0.1)
    prob = np.clip(prob, 0.05, 0.95)
    churn = (np.random.rand(n) < prob).astype(int)

    churn_df = pd.DataFrame({
        "tenure": tenure,
        "monthly_charges": monthly_charges,
        "total_charges": total_charges,
        "contract": contract,
        "support_tickets": support_tickets,
        "churn": churn
    })
    churn_path = "demo_data/customer_churn_benchmark.csv"
    churn_df.to_csv(churn_path, index=False)
    print(f"Generated: {churn_path} ({len(churn_df)} rows)")

    # 2. Sensor Equipment Faults
    n_sensor = 800
    temp = np.round(np.random.normal(75.0, 12.0, size=n_sensor), 2)
    vibration = np.round(np.random.exponential(1.5, size=n_sensor), 3)
    pressure = np.round(np.random.normal(101.3, 5.0, size=n_sensor), 2)
    fault = ((temp > 90.0) | (vibration > 4.0)).astype(int)

    sensor_df = pd.DataFrame({
        "temperature_c": temp,
        "vibration_rms": vibration,
        "pressure_kpa": pressure,
        "fault_detected": fault
    })
    sensor_path = "demo_data/sensor_faults_benchmark.csv"
    sensor_df.to_csv(sensor_path, index=False)
    print(f"Generated: {sensor_path} ({len(sensor_df)} rows)")

if __name__ == "__main__":
    generate_datasets()
