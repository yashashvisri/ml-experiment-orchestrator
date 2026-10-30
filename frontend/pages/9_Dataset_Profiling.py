import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.auth import init_session, is_authenticated
from utils.api import api_get
from utils.styles import apply_custom_styles

st.set_page_config(page_title="Dataset Profiling & EDA", page_icon="📈", layout="wide")

apply_custom_styles()
init_session()

if not is_authenticated():
    st.warning("Please log in from the main page to profile datasets.")
    st.stop()

st.title("📈 Automated Dataset Profiling & EDA Studio")
st.caption("Deep-dive exploratory data analysis: summary health metrics, missing value audits, correlation matrices, and AI recommendations.")

# Project & Dataset selectors
resp = api_get("/projects/", token=st.session_state.token)
if resp.status_code != 200:
    st.error("Failed to fetch projects.")
    st.stop()

projects = resp.json()
if not projects:
    st.info("You need to create a Project first before profiling datasets.")
    st.stop()

project_map = {p['name']: p['id'] for p in projects}
selected_project_name = st.selectbox("Select Project Workspace", options=list(project_map.keys()))
selected_project_id = project_map[selected_project_name]

ds_resp = api_get(f"/projects/{selected_project_id}/datasets", token=st.session_state.token)
datasets = ds_resp.json() if ds_resp.status_code == 200 else []

if not datasets:
    st.info("No datasets uploaded to this project yet. Upload a CSV file in the Datasets tab.")
    st.stop()

dataset_map = {d['name']: d['id'] for d in datasets}
selected_dataset_name = st.selectbox("Select Dataset to Profile", options=list(dataset_map.keys()))
selected_dataset_id = dataset_map[selected_dataset_name]

st.divider()

with st.spinner("Analyzing dataset distribution and computing correlation matrix..."):
    profile_resp = api_get(f"/projects/{selected_project_id}/datasets/{selected_dataset_id}/profile", token=st.session_state.token)

if profile_resp.status_code != 200:
    st.error(f"Failed to profile dataset: {profile_resp.text}")
    st.stop()

profile = profile_resp.json()
summary = profile.get("summary", {})
columns = profile.get("columns", [])
corr_data = profile.get("correlation", {})

# KPI Cards
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-card-label">Total Rows</div>
        <div class="metric-card-val">{summary.get('total_rows', 0):,}</div>
        <div class="metric-badge">📋 Observations</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-card-label">Features Count</div>
        <div class="metric-card-val">{summary.get('total_columns', 0)}</div>
        <div class="metric-badge">🔢 {summary.get('numeric_columns_count', 0)} Num / {summary.get('categorical_columns_count', 0)} Cat</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    miss_pct = summary.get('total_missing_cells_pct', 0.0)
    color = "#10b981" if miss_pct < 5.0 else ("#f59e0b" if miss_pct < 20.0 else "#ef4444")
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-card-label">Missing Cells</div>
        <div class="metric-card-val" style="color: {color};">{miss_pct}%</div>
        <div class="metric-badge">{summary.get('total_missing_cells', 0):,} Nulls</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-card-label">Memory Footprint</div>
        <div class="metric-card-val">{summary.get('memory_usage_kb', 0)} KB</div>
        <div class="metric-badge">💾 In-Memory</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.divider()

