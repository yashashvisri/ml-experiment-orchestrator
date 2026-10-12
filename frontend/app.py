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
