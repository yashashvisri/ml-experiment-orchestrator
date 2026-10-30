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

# Tabbed EDA View
tab_dist, tab_corr, tab_missing = st.tabs(["📊 Feature Distributions", "🔥 Correlation Heatmap", "⚠️ Missingness Audit"])

with tab_dist:
    st.subheader("Feature Level Diagnostics")
    col_names = [c["name"] for c in columns]
    if col_names:
        sel_col_name = st.selectbox("Select Feature to Inspect", options=col_names)
        sel_col = next(c for c in columns if c["name"] == sel_col_name)
        
        d1, d2, d3, d4 = st.columns(4)
        d1.metric("Data Type", sel_col["dtype"])
        d2.metric("Distinct Values", sel_col["unique_count"])
        d3.metric("Missing Values", f"{sel_col['missing_count']} ({sel_col['missing_pct']}%)")
        d4.metric("Skewness", str(sel_col["skewness"]) if sel_col["skewness"] is not None else "N/A")

        if sel_col.get("mean") is not None:
            st.markdown(f"**Mean:** `{sel_col['mean']}` | **Std:** `{sel_col['std']}` | **Min:** `{sel_col['min']}` | **Median:** `{sel_col['median']}` | **Max:** `{sel_col['max']}` | **Outliers (IQR):** `{sel_col.get('outlier_count', 0)}`")
        elif sel_col.get("top_values"):
            st.markdown("**Top Category Frequencies:**")
            st.bar_chart(pd.DataFrame(list(sel_col["top_values"].items()), columns=["Category", "Count"]).set_index("Category"))

with tab_corr:
    st.subheader("Pearson Correlation Matrix (Numeric Features)")
    corr_cols = corr_data.get("columns", [])
    corr_matrix = corr_data.get("matrix", [])
    if corr_cols and corr_matrix:
        fig_corr = px.imshow(
            corr_matrix,
            x=corr_cols,
            y=corr_cols,
            color_continuous_scale="RdBu_r",
            zmin=-1.0,
            zmax=1.0,
            text_auto=True,
            title="Interactive Feature Correlation Heatmap"
        )
        fig_corr.update_layout(
            template="plotly_dark",
            paper_bgcolor="#161f30",
            plot_bgcolor="#0b0f19",
            font=dict(color="#f8fafc", family="Plus Jakarta Sans"),
            height=500
        )
        st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.info("Insufficient numeric columns to compute a correlation matrix.")

with tab_missing:
    st.subheader("Missing Value Frequency by Feature")
    miss_df = pd.DataFrame([{
        "Feature": c["name"],
        "Missing %": c["missing_pct"],
        "Missing Count": c["missing_count"]
    } for c in columns if c["missing_count"] > 0])

    if not miss_df.empty:
        fig_miss = px.bar(
            miss_df,
            x="Feature",
            y="Missing %",
            color="Missing %",
            color_continuous_scale="Reds",
            title="Features with Missing Values (%)",
            text_auto=".1f"
        )
        fig_miss.update_layout(
            template="plotly_dark",
            paper_bgcolor="#161f30",
            plot_bgcolor="#0b0f19",
            font=dict(color="#f8fafc", family="Plus Jakarta Sans")
        )
        st.plotly_chart(fig_miss, use_container_width=True)
    else:
        st.success("🎉 Zero missing values detected across all features!")

