import streamlit as st
import pandas as pd
from utils.auth import init_session, is_authenticated
from utils.api import api_get, api_post

st.set_page_config(page_title="Runs", page_icon="🏃")

init_session()

if not is_authenticated():
    st.warning("Please log in from the main page to access Runs.")
    st.stop()

st.title("🏃 MLflow Runs")

# Fetch projects
resp = api_get("/projects/", token=st.session_state.token)
if resp.status_code != 200:
    st.error("Failed to fetch projects.")
    st.stop()

projects = resp.json()
if not projects:
    st.info("You need to create a Project first.")
    st.stop()

project_map = {p['name']: p['id'] for p in projects}
selected_project_name = st.selectbox("Select Project", options=list(project_map.keys()))
selected_project_id = project_map[selected_project_name]

# Fetch experiments
exp_resp = api_get(f"/projects/{selected_project_id}/experiments", token=st.session_state.token)
if exp_resp.status_code != 200:
    st.error("Failed to fetch experiments.")
    st.stop()

experiments = exp_resp.json()
if not experiments:
    st.info("You need to create an Experiment first before logging runs.")
    st.stop()

exp_map = {e['name']: e['id'] for e in experiments}
selected_exp_name = st.selectbox("Select Experiment", options=list(exp_map.keys()))
selected_exp_id = exp_map[selected_exp_name]

st.divider()

# Create Run
st.subheader("Log a New Run")
st.caption("Normally runs are logged automatically via Python scripts. Use this to manually register a run in MLflow.")
with st.form("create_run_form", clear_on_submit=True):
    r_name = st.text_input("Run Name (required)")
    
    submit_create = st.form_submit_button("Log Run")
    if submit_create:
        if not r_name:
            st.error("Run Name is required.")
        else:
            data = {"name": r_name}
            with st.spinner("Logging..."):
                create_resp = api_post(f"/experiments/{selected_exp_id}/runs", json=data, token=st.session_state.token)
            
            if create_resp.status_code == 200:
                st.success("Run logged successfully!")
                st.rerun()
            else:
                st.error(f"Failed: {create_resp.text}")

st.divider()

# List Runs
st.subheader("Experiment Runs")
runs_resp = api_get(f"/experiments/{selected_exp_id}/runs", token=st.session_state.token)
if runs_resp.status_code == 200:
    runs = runs_resp.json()
    if not runs:
        st.info("No runs logged yet for this experiment.")
    else:
        df_data = []
        for r in runs:
            df_data.append({
                "Run Name": r["name"],
                "Status": r["status"],
                "MLflow Run ID": r["mlflow_run_id"],
                "Logged At": r["created_at"][:19],
            })
        st.dataframe(pd.DataFrame(df_data), use_container_width=True)
else:
    st.error("Failed to fetch runs.")

