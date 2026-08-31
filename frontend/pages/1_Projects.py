import streamlit as st
from utils.auth import init_session, is_authenticated
from utils.api import api_get, api_post, api_delete

st.set_page_config(page_title="Projects", page_icon="📁")

init_session()

if not is_authenticated():
    st.warning("Please log in from the main page to access Projects.")
    st.stop()

st.title("📁 Projects")

# Create Project Form
with st.expander("➕ Create New Project", expanded=False):
    with st.form("create_project_form"):
        p_name = st.text_input("Project Name")
        p_desc = st.text_area("Description")
        submit_create = st.form_submit_button("Create")
        
        if submit_create:
            if not p_name:
                st.error("Project Name is required.")
            else:
                resp = api_post("/projects/", json={"name": p_name, "description": p_desc}, token=st.session_state.token)
                if resp.status_code == 200:
                    st.success("Project created successfully!")
                    st.rerun()
                else:
                    st.error(f"Error creating project: {resp.text}")

st.divider()

# List Projects
st.subheader("Your Projects")
resp = api_get("/projects/", token=st.session_state.token)
if resp.status_code == 200:
    projects = resp.json()
    if not projects:
        st.info("You don't have any projects yet.")
    else:
        for p in projects:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"### {p['name']}")
                if p['description']:
                    st.write(p['description'])
                st.caption(f"Created: {p['created_at'][:10]} | ID: {p['id']}")
            with col2:
                if st.button("Delete", key=f"del_{p['id']}", type="primary"):
                    del_resp = api_delete(f"/projects/{p['id']}", token=st.session_state.token)
                    if del_resp.status_code == 200:
                        st.success("Deleted!")
                        st.rerun()
                    else:
                        st.error("Failed to delete.")
            st.divider()
else:
    st.error("Failed to fetch projects.")
