import streamlit as st
import requests
from utils.auth import init_session, is_authenticated
from utils.api import api_get
from utils.styles import apply_custom_styles

st.set_page_config(page_title="AI Reports", page_icon="📑", layout="wide")

apply_custom_styles()
init_session()

if not is_authenticated():
    st.warning("Please log in from the main page to generate AI Reports.")
    st.stop()

st.title("📑 Automated AI Reports")
st.caption("Generate executive summaries, model comparison tables, and downloadable PDF reports powered by AI.")

# Select Project
resp = api_get("/projects/", token=st.session_state.token)
if resp.status_code != 200:
    st.error("Failed to fetch projects.")
    st.stop()

projects = resp.json()
if not projects:
    st.info("You need to create a Project first before generating reports.")
    st.stop()

project_map = {p['name']: p['id'] for p in projects}
selected_project_name = st.selectbox("Select Project Workspace", options=list(project_map.keys()))
selected_project_id = project_map[selected_project_name]

# Select optional experiment filter
exp_resp = api_get(f"/projects/{selected_project_id}/experiments", token=st.session_state.token)
experiments = exp_resp.json() if exp_resp.status_code == 200 else []
exp_options = {"All Experiments": None}
for e in experiments:
    exp_options[e["name"]] = e["id"]

selected_exp_label = st.selectbox("Filter by Experiment (Optional)", options=list(exp_options.keys()))
selected_exp_id = exp_options[selected_exp_label]

st.divider()

col_btn, col_info = st.columns([2, 5])
with col_btn:
    generate_btn = st.button("🚀 Generate AI Experiment Report", type="primary", use_container_width=True)

with col_info:
    st.caption("AI analyzes training telemetry, hyperparameters, and MLflow loss curves to synthesize executive takeaways.")

if "report_data" not in st.session_state:
    st.session_state.report_data = None
