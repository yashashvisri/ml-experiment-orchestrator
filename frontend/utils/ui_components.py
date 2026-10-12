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

def render_hero_header(title: str, subtitle: str):
    """Renders a gradient hero header and subtitle."""
    st.markdown(f'<h1 class="hero-title">{title}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="hero-subtitle">{subtitle}</p>', unsafe_allow_html=True)
