import streamlit as st
from utils.api import api_post, api_get

def init_session():
    if "token" not in st.session_state:
        st.session_state.token = None
    if "user" not in st.session_state:
        st.session_state.user = None

def login(email, password):
    response = api_post("/auth/login", json={"email": email, "password": password})
    if response.status_code == 200:
        data = response.json()
        st.session_state.token = data.get("access_token")
        _fetch_current_user()
        return True, "Login successful!"
    return False, response.json().get("detail", "Login failed")

def register(email, password, full_name):
    payload = {
        "email": email,
        "password": password,
        "full_name": full_name
    }
    response = api_post("/auth/register", json=payload)
    if response.status_code == 200:
        return True, "Registration successful! You can now login."
    return False, response.json().get("detail", "Registration failed")

def _fetch_current_user():
    if st.session_state.token:
        response = api_get("/auth/me", token=st.session_state.token)
        if response.status_code == 200:
            st.session_state.user = response.json()
        else:
            logout()

def logout():
    st.session_state.token = None
    st.session_state.user = None

def is_authenticated():
    return st.session_state.token is not None
