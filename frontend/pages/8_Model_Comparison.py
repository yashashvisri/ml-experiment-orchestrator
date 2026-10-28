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

# Fetch Comparison Data
params = {}
if selected_exp_id:
    params["experiment_id"] = selected_exp_id

comp_resp = api_get(f"/comparison/{selected_project_id}", token=st.session_state.token, params=params)
if comp_resp.status_code != 200:
    st.error(f"Failed to fetch model comparison: {comp_resp.text}")
    st.stop()

data = comp_resp.json()
runs = data.get("runs", [])

if not runs:
    st.info("No runs found for this workspace. Train models via AutoML or log MLflow runs first!")
    st.stop()

# Champion & Metrics Cards
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-card-label">Total Models</div>
        <div class="metric-card-val">{len(runs)}</div>
        <div class="metric-badge">🧪 Evaluated</div>
    </div>
    """, unsafe_allow_html=True)

champion_metric = data.get("champion_metric")
champ_str = f"{champion_metric * 100:.2f}%" if champion_metric is not None else "N/A"
with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-card-label">Top Benchmark Score</div>
        <div class="metric-card-val">{champ_str}</div>
        <div class="metric-badge">🏆 Accuracy</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    num_params = len(data.get("param_keys", []))
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-card-label">Tuned Parameters</div>
        <div class="metric-card-val">{num_params}</div>
        <div class="metric-badge">⚡ Optuna Space</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-card-label">Frameworks</div>
        <div class="metric-card-val">3</div>
        <div class="metric-badge">🌲 XGB/LGBM/RF</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.divider()

st.subheader("📊 Performance Metric Comparison")
metric_keys = data.get("metric_keys", ["accuracy"])
selected_metric = st.selectbox("Select Target Metric to Compare", options=metric_keys if metric_keys else ["accuracy"])

chart_data = []
for r in runs:
    val = r.get("metrics", {}).get(selected_metric, 0.0)
    chart_data.append({
        "Run Name": r["run_name"],
        "Experiment": r["experiment_name"],
        selected_metric: val,
        "Status": r["status"]
    })

df_chart = pd.DataFrame(chart_data)
if not df_chart.empty:
    fig_bar = px.bar(
        df_chart,
        x="Run Name",
        y=selected_metric,
        color=selected_metric,
        color_continuous_scale="Viridis",
        title=f"Comparison of {selected_metric.capitalize()} across Runs",
        text_auto=".3f"
    )
    fig_bar.update_layout(
        template="plotly_dark",
        paper_bgcolor="#161f30",
        plot_bgcolor="#0b0f19",
        font=dict(color="#f8fafc", family="Plus Jakarta Sans"),
        margin=dict(l=40, r=40, t=50, b=40)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

st.subheader("🔍 Side-by-Side Model Hyperparameter Diff")
run_names = [r["run_name"] for r in runs]
if len(run_names) >= 2:
    diff_col1, diff_col2 = st.columns(2)
    with diff_col1:
        run_a_name = st.selectbox("Model A", options=run_names, index=0)
    with diff_col2:
        run_b_name = st.selectbox("Model B", options=run_names, index=1 if len(run_names) > 1 else 0)

    run_a = next(r for r in runs if r["run_name"] == run_a_name)
    run_b = next(r for r in runs if r["run_name"] == run_b_name)

    all_keys = sorted(list(set(run_a.get("params", {}).keys()).union(set(run_b.get("params", {}).keys()))))
    diff_rows = []
    for k in all_keys:
        val_a = run_a.get("params", {}).get(k, "-")
        val_b = run_b.get("params", {}).get(k, "-")
        is_diff = "⚠️ Different" if str(val_a) != str(val_b) else "✅ Identical"
        diff_rows.append({"Parameter": k, run_a_name: str(val_a), run_b_name: str(val_b), "Status": is_diff})

    st.dataframe(pd.DataFrame(diff_rows), use_container_width=True)
else:
    st.info("Log at least 2 runs to compare hyperparameters side-by-side.")

st.divider()

st.subheader("📋 Comprehensive Runs Leaderboard")
table_data = []
for r in runs:
    row = {
        "Run Name": r["run_name"],
        "Experiment": r["experiment_name"],
        "Status": r["status"],
        "Logged At": r["logged_at"]
    }
    for m in data.get("metric_keys", []):
        row[f"Metric: {m}"] = r.get("metrics", {}).get(m, None)
    for p in data.get("param_keys", [])[:5]:
        row[f"Param: {p}"] = r.get("params", {}).get(p, None)
    table_data.append(row)

st.dataframe(pd.DataFrame(table_data), use_container_width=True)
