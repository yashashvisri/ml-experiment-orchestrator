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

if generate_btn:
    params = {}
    if selected_exp_id:
        params["experiment_id"] = selected_exp_id

    with st.spinner("Analyzing runs and compiling AI report..."):
        r_resp = api_get(f"/reports/{selected_project_id}/summary", token=st.session_state.token, params=params)
    
    if r_resp.status_code == 200:
        st.session_state.report_data = r_resp.json()
        st.success("Report generated successfully!")
    else:
        st.error(f"Failed to generate report: {r_resp.text}")

if st.session_state.report_data:
    rep = st.session_state.report_data
    
    st.subheader("Overview KPI Snapshot")
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-label">Project Workspace</div>
            <div class="metric-card-val" style="font-size: 1.25rem;">{rep.get('project_name')}</div>
            <div class="metric-badge">📁 Active</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-label">Total Evaluated Runs</div>
            <div class="metric-card-val">{rep.get('total_runs', 0)}</div>
            <div class="metric-badge">🧪 MLflow</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        champion = rep.get('best_model_name') or 'N/A'
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-label">Top Champion Model</div>
            <div class="metric-card-val" style="font-size: 1.15rem;">{champion[:18]}</div>
            <div class="metric-badge">🏆 Best Performer</div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        best_metrics = rep.get('best_metric') or {}
        acc = best_metrics.get('accuracy')
        acc_str = f"{acc * 100:.2f}%" if isinstance(acc, (int, float)) else "N/A"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-label">Validation Accuracy</div>
            <div class="metric-card-val">{acc_str}</div>
            <div class="metric-badge">⚡ Optuna Tuned</div>
        </div>
        """, unsafe_allow_html=True)
    st.write("")

    st.divider()
    
    col_dl1, col_dl2 = st.columns([1, 1])
    with col_dl1:
        st.download_button(
            label="📥 Download Markdown Report (.md)",
            data=rep.get("markdown_content", ""),
            file_name=f"report_{selected_project_name.lower().replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True
        )

    with col_dl2:
        # Fetch PDF binary directly
        pdf_url = f"http://localhost:8000/api/v1/reports/{selected_project_id}/pdf"
        if selected_exp_id:
            pdf_url += f"?experiment_id={selected_exp_id}"
        
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        pdf_resp = requests.get(pdf_url, headers=headers)
        if pdf_resp.status_code == 200:
            st.download_button(
                label="📄 Download Executive PDF Report (.pdf)",
                data=pdf_resp.content,
                file_name=f"report_{selected_project_name.lower().replace(' ', '_')}.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True
            )
        else:
            st.button("PDF Generator Error", disabled=True, use_container_width=True)

    st.write("")
    st.subheader("📑 Report Document Preview")
    with st.container():
        st.markdown(rep.get("markdown_content", ""))
