import streamlit as st
import pandas as pd
from utils.auth import init_session, is_authenticated
from utils.api import api_get, api_post

st.set_page_config(page_title="Experiments", page_icon="🧪")

init_session()

if not is_authenticated():
    st.warning("Please log in from the main page to access Experiments.")
    st.stop()

st.title("🧪 Experiments")

# Fetch projects for dropdown
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

# Create Experiment
st.subheader("Create New Experiment")
with st.form("create_experiment_form", clear_on_submit=True):
    e_name = st.text_input("Experiment Name (required)")
    e_desc = st.text_area("Description (optional)")
    
    submit_create = st.form_submit_button("Create")
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

st.divider()

# List Experiments
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

