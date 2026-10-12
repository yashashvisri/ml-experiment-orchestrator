import streamlit as st
from utils.auth import init_session, is_authenticated, login, register, logout
from utils.styles import apply_custom_styles
from utils.api import api_get

st.set_page_config(
    page_title="ML Experiment Orchestrator",
    page_icon="🚀",
    layout="wide"
)

apply_custom_styles()
init_session()

if is_authenticated():
    user_name = st.session_state.user.get('full_name') or st.session_state.user.get('email', 'User')
    
    top_col1, top_col2 = st.columns([5, 1])
    with top_col1:
        st.markdown(f'<h1 class="hero-title">ML Experiment Orchestrator 🚀</h1>', unsafe_allow_html=True)
        st.markdown(f'<p class="hero-subtitle">Welcome back, <span style="color:#a5b4fc; font-weight:600;">{user_name}</span> • Production AI Experimentation & AutoML Platform</p>', unsafe_allow_html=True)
    with top_col2:
        st.write("")
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()

    c1, c2, c3, c4 = st.columns(4)
    projects_count = 0
    p_resp = api_get("/projects/", token=st.session_state.token)
    if p_resp.status_code == 200:
        projects_count = len(p_resp.json())

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-label">Active Projects</div>
            <div class="metric-card-val">{projects_count}</div>
            <div class="metric-badge">📁 PostgreSQL</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-card-label">MLflow Tracking</div>
            <div class="metric-card-val">Live</div>
            <div class="metric-badge">🧪 SQLite / Local</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-card-label">AutoML Engine</div>
            <div class="metric-card-val">Optuna</div>
            <div class="metric-badge">⚡ XGB / LGBM / RF</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-card-label">AI Agent Brain</div>
            <div class="metric-card-val">Gemini 1.5</div>
            <div class="metric-badge">🤖 LangGraph + RAG</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.divider()

    st.subheader("⚡ Quick Launch Hub")
    q1, q2, q3 = st.columns(3)

    with q1:
        with st.container():
            st.markdown("""
            <div class="metric-card" style="margin-bottom: 0.75rem;">
                <h4 style="margin: 0; color: #f8fafc;">📁 Projects & Datasets</h4>
                <p style="color: #94a3b8; font-size: 0.85rem; margin-top: 0.25rem;">
                    Manage experiment workspaces, upload CSV training data, and review dataset schemas.
                </p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Open Projects →", key="btn_proj", use_container_width=True):
                st.switch_page("pages/1_Projects.py")

    with q2:
        with st.container():
            st.markdown("""
            <div class="metric-card" style="margin-bottom: 0.75rem;">
                <h4 style="margin: 0; color: #f8fafc;">🧪 AutoML & Experiments</h4>
                <p style="color: #94a3b8; font-size: 0.85rem; margin-top: 0.25rem;">
                    Trigger Optuna hyperparameter optimization runs, view metrics, and inspect MLflow logs.
                </p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Launch AutoML Studio →", key="btn_exp", use_container_width=True):
                st.switch_page("pages/3_Experiments.py")

    with q3:
        with st.container():
            st.markdown("""
            <div class="metric-card" style="margin-bottom: 0.75rem;">
                <h4 style="margin: 0; color: #f8fafc;">🤖 AI Assistant & Knowledge Base</h4>
                <p style="color: #94a3b8; font-size: 0.85rem; margin-top: 0.25rem;">
                    Chat with your LangGraph AI Data Scientist and index PDFs via FAISS vector search.
                </p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Talk to AI Assistant →", key="btn_agent", use_container_width=True):
                st.switch_page("pages/5_AI_Assistant.py")
