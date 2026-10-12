import streamlit as st
import pandas as pd
from utils.auth import init_session, is_authenticated
from utils.api import api_get, api_post
from utils.styles import apply_custom_styles

st.set_page_config(page_title="Experiments", page_icon="🧪", layout="wide")

apply_custom_styles()
init_session()

if not is_authenticated():
    st.warning("Please log in from the main page to access Experiments.")
    st.stop()

st.title("🧪 Experiments & AutoML")

resp = api_get("/projects/", token=st.session_state.token)
if resp.status_code != 200:
    st.error("Failed to fetch projects.")
    st.stop()

projects = resp.json()
if not projects:
    st.info("You need to create a Project first before creating experiments.")
    st.stop()

project_map = {p['name']: p['id'] for p in projects}
selected_project_name = st.selectbox("Select Project", options=list(project_map.keys()))
selected_project_id = project_map[selected_project_name]

st.divider()

col_e1, col_e2 = st.columns(2)

with col_e1:
    st.subheader("Create New Experiment")
    with st.form("create_experiment_form", clear_on_submit=True):
        e_name = st.text_input("Experiment Name (required)")
        e_desc = st.text_area("Description (optional)")
        
        submit_create = st.form_submit_button("Create Experiment", type="primary")
        if submit_create:
            if not e_name:
                st.error("Experiment Name is required.")
            else:
                data = {"name": e_name, "description": e_desc or ""}
                with st.spinner("Creating..."):
                    create_resp = api_post(f"/projects/{selected_project_id}/experiments", json=data, token=st.session_state.token)
                
                if create_resp.status_code == 200:
                    st.success("Experiment created successfully!")
                    st.rerun()
                else:
                    st.error(f"Failed: {create_resp.text}")

with col_e2:
    st.subheader("Start AutoML Training")
    with st.form("train_automl_form"):
        ds_resp = api_get(f"/projects/{selected_project_id}/datasets", token=st.session_state.token)
        datasets = []
        if ds_resp.status_code == 200:
            datasets = ds_resp.json()
            
        if not datasets:
            st.warning("No datasets found. Please upload a dataset first.")
            st.form_submit_button("Start Training", disabled=True)
        else:
            dataset_map = {d['name']: d['id'] for d in datasets}
            selected_ds_name = st.selectbox("Select Dataset", options=list(dataset_map.keys()))
            target_col = st.text_input("Target Column Name", value="target")
            model_type = st.selectbox("Model Type", ["xgboost", "lightgbm", "random_forest"])
            n_trials = st.slider("Number of Optuna Trials", min_value=1, max_value=50, value=10)
            
            exp_resp = api_get(f"/projects/{selected_project_id}/experiments", token=st.session_state.token)
            experiments_for_train = []
            if exp_resp.status_code == 200:
                experiments_for_train = exp_resp.json()
                
            if not experiments_for_train:
                st.warning("Please create an experiment first.")
                st.form_submit_button("Start Training", disabled=True)
            else:
                exp_map = {e['name']: e['id'] for e in experiments_for_train}
                selected_exp_train = st.selectbox("Log to Experiment", options=list(exp_map.keys()))
                
                submit_train = st.form_submit_button("Start Training 🚀", type="primary")
                if submit_train:
                    train_data = {
                        "dataset_id": dataset_map[selected_ds_name],
                        "target_column": target_col,
                        "model_type": model_type,
                        "n_trials": n_trials
                    }
                    with st.spinner("Starting training job in background..."):
                        t_resp = api_post(f"/experiments/{exp_map[selected_exp_train]}/train", json=train_data, token=st.session_state.token)
                    
                    if t_resp.status_code == 200:
                        st.success("Training job started in the background! Check the Runs page.")
                    else:
                        st.error(f"Failed to start training: {t_resp.text}")

st.divider()

st.subheader("Project Experiments")
exp_resp = api_get(f"/projects/{selected_project_id}/experiments", token=st.session_state.token)
if exp_resp.status_code == 200:
    experiments = exp_resp.json()
    if not experiments:
        st.info("No experiments found for this project.")
    else:
        df_data = []
        for e in experiments:
            df_data.append({
                "Name": e["name"],
                "Description": e["description"],
                "MLflow ID": e["mlflow_experiment_id"],
                "Created At": e["created_at"][:19],
            })
        st.dataframe(pd.DataFrame(df_data), use_container_width=True)
else:
    st.error("Failed to fetch experiments.")
