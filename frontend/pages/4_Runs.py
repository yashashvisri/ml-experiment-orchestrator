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

