import streamlit as st
import pandas as pd
from utils.auth import init_session, is_authenticated
from utils.api import api_get, api_post

st.set_page_config(page_title="Experiments", page_icon="🧪")

init_session()

if not is_authenticated():
    st.warning("Please log in from the main page to access Experiments.")
    st.stop()

st.title("🧪 Experiments")

