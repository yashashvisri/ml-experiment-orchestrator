import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.auth import init_session, is_authenticated
from utils.api import api_get
from utils.styles import apply_custom_styles

st.set_page_config(page_title="Model Comparison", page_icon="⚖️", layout="wide")

apply_custom_styles()
init_session()

if not is_authenticated():
    st.warning("Please log in from the main page to compare models.")
    st.stop()

st.title("⚖️ Model Comparison & Leaderboard")
st.caption("Compare performance metrics, hyperparameters, and trade-offs across experiments and AutoML trials.")

# Fetch projects
resp = api_get("/projects/", token=st.session_state.token)
if resp.status_code != 200:
    st.error("Failed to fetch projects.")
    st.stop()

projects = resp.json()
if not projects:
    st.info("You need to create a Project first before comparing models.")
    st.stop()

project_map = {p['name']: p['id'] for p in projects}
selected_project_name = st.selectbox("Select Project Workspace", options=list(project_map.keys()))
selected_project_id = project_map[selected_project_name]

# Optional Experiment Filter
exp_resp = api_get(f"/projects/{selected_project_id}/experiments", token=st.session_state.token)
experiments = exp_resp.json() if exp_resp.status_code == 200 else []
exp_options = {"All Experiments": None}
for e in experiments:
    exp_options[e["name"]] = e["id"]

selected_exp_label = st.selectbox("Filter Experiment", options=list(exp_options.keys()))
selected_exp_id = exp_options[selected_exp_label]

st.divider()
