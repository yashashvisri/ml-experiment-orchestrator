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

def render_quick_action_card(title: str, description: str):
    """Renders a styled quick action card for dashboard navigation."""
    st.markdown(f"""
    <div class="metric-card" style="margin-bottom: 0.75rem;">
        <h4 style="margin: 0; color: #f8fafc;">{title}</h4>
        <p style="color: #94a3b8; font-size: 0.85rem; margin-top: 0.25rem;">
            {description}
        </p>
    </div>
    """, unsafe_allow_html=True)
