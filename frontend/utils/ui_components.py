"""Reusable UI components for Streamlit ML Orchestrator."""
import streamlit as st

def render_metric_card(label: str, value: str, badge: str):
    """Renders a styled KPI metric card with a badge."""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-card-label">{label}</div>
        <div class="metric-card-val">{value}</div>
        <div class="metric-badge">{badge}</div>
    </div>
    """, unsafe_allow_html=True)
