import streamlit as st
from utils.auth import init_session, is_authenticated
from utils.api import api_post

st.set_page_config(page_title="AI Assistant", page_icon="🤖")
init_session()

if not is_authenticated():
    st.warning("Please log in to chat with the AI Assistant.")
    st.stop()

st.title("🤖 AI Experiment Assistant")
st.caption("Ask me about your projects, experiments, or MLflow runs! (Requires OPENAI_API_KEY in backend .env)")

