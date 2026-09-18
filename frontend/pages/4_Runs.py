import streamlit as st
import pandas as pd
from utils.auth import init_session, is_authenticated
from utils.api import api_get, api_post

st.set_page_config(page_title="Runs", page_icon="🏃")

