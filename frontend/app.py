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
    q1, q2, q3, q4, q5, q6 = st.columns(6)

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

    with q4:
        with st.container():
            st.markdown("""
            <div class="metric-card" style="margin-bottom: 0.75rem;">
                <h4 style="margin: 0; color: #f8fafc;">📑 Automated Reports</h4>
                <p style="color: #94a3b8; font-size: 0.85rem; margin-top: 0.25rem;">
                    Export executive experiment briefs and performance audits in PDF or Markdown format.
                </p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Generate Reports →", key="btn_reports", use_container_width=True):
                st.switch_page("pages/7_Reports.py")

    with q5:
        with st.container():
            st.markdown("""
            <div class="metric-card" style="margin-bottom: 0.75rem;">
                <h4 style="margin: 0; color: #f8fafc;">⚖️ Model Comparison</h4>
                <p style="color: #94a3b8; font-size: 0.85rem; margin-top: 0.25rem;">
                    Compare Optuna hyperparameter trials, metrics, and side-by-side diffs.
                </p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Compare Models →", key="btn_compare", use_container_width=True):
                st.switch_page("pages/8_Model_Comparison.py")

    with q6:
        with st.container():
            st.markdown("""
            <div class="metric-card" style="margin-bottom: 0.75rem;">
                <h4 style="margin: 0; color: #f8fafc;">📈 Dataset Profiling</h4>
                <p style="color: #94a3b8; font-size: 0.85rem; margin-top: 0.25rem;">
                    Automated EDA: missingness audits, correlation heatmaps, and AI diagnostics.
                </p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Profile Datasets →", key="btn_profile", use_container_width=True):
                st.switch_page("pages/9_Dataset_Profiling.py")

else:
    col_center1, col_center2, col_center3 = st.columns([1, 2, 1])
    with col_center2:
        st.markdown('<div style="text-align: center; margin-top: 2rem;">', unsafe_allow_html=True)
        st.markdown('<h1 class="hero-title" style="text-align: center;">ML Experiment Orchestrator</h1>', unsafe_allow_html=True)
        st.markdown('<p class="hero-subtitle" style="text-align: center;">Sign in to your production AI experiment workspace</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔐 Sign In", "✨ Create Account"])
        
        with tab1:
            with st.form("login_form"):
                email = st.text_input("Work Email", placeholder="researcher@lab.ai")
                password = st.text_input("Password", type="password", placeholder="••••••••")
                submit = st.form_submit_button("Sign In →", type="primary", use_container_width=True)
                
                if submit:
                    if not email or not password:
                        st.error("Please fill in both email and password.")
                    else:
                        with st.spinner("Authenticating..."):
                            success, msg = login(email, password)
                        if success:
                            st.success("Welcome back!")
                            st.rerun()
                        else:
                            st.error(msg)
                        
        with tab2:
            with st.form("register_form"):
                reg_name = st.text_input("Full Name", placeholder="Dr. Jane Doe")
                reg_email = st.text_input("Email", placeholder="jane@lab.ai")
                reg_password = st.text_input("Password", type="password", placeholder="Create a secure password")
                submit_reg = st.form_submit_button("Register Account →", type="primary", use_container_width=True)
                
                if submit_reg:
                    if not reg_email or not reg_password:
                        st.error("Email and password are required.")
                    else:
                        with st.spinner("Creating account..."):
                            success, msg = register(reg_email, reg_password, reg_name)
                        if success:
                            st.success("Account created successfully! Please switch to the Sign In tab.")
                        else:
                            st.error(msg)
