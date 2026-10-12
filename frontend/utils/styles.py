import streamlit as st

def apply_custom_styles():
    """Injects high-end, modern CSS styling across all Streamlit pages."""
    st.markdown("<style></style>", unsafe_allow_html=True)
