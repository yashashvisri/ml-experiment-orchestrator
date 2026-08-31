import streamlit as st
from utils.auth import init_session, is_authenticated, login, register, logout

st.set_page_config(
    page_title="ML Experiment Orchestrator",
    page_icon="🚀",
    layout="centered"
)

init_session()

if is_authenticated():
    st.title("Welcome to ML Experiment Orchestrator! 🚀")
    st.write(f"Logged in as: **{st.session_state.user.get('full_name', st.session_state.user.get('email'))}**")
    
    st.success("You are successfully authenticated.")
    st.info("👈 Please use the sidebar to navigate to **Projects** and **Datasets**.")
    
    if st.button("Logout"):
        logout()
        st.rerun()

else:
    st.title("ML Experiment Orchestrator 🔐")
    st.write("Please login or register to continue.")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                success, msg = login(email, password)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
                    
    with tab2:
        st.subheader("Register")
        with st.form("register_form"):
            reg_name = st.text_input("Full Name")
            reg_email = st.text_input("Email")
            reg_password = st.text_input("Password", type="password")
            submit_reg = st.form_submit_button("Register")
            
            if submit_reg:
                success, msg = register(reg_email, reg_password, reg_name)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)
