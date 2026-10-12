import streamlit as st
from utils.auth import init_session, is_authenticated
from utils.api import api_get
from utils.styles import apply_custom_styles
import requests
import os

st.set_page_config(page_title="Knowledge Base", page_icon="📚", layout="wide")

apply_custom_styles()
init_session()

if not is_authenticated():
    st.warning("Please log in to upload documents to the Knowledge Base.")
    st.stop()

st.title("📚 Project Knowledge Base")
st.caption("Upload PDF documents, papers, and logs so your AI Assistant can search through them using RAG (FAISS + Google Embeddings)!")

resp = api_get("/projects/", token=st.session_state.token)
if resp.status_code != 200:
    st.error("Failed to fetch projects.")
    st.stop()

projects = resp.json()
if not projects:
    st.info("You need to create a Project first.")
    st.stop()

project_map = {p['name']: p['id'] for p in projects}
selected_project_name = st.selectbox("Select Project", options=list(project_map.keys()))
selected_project_id = project_map[selected_project_name]

st.divider()

uploaded_file = st.file_uploader("Upload a PDF document for RAG indexing", type=["pdf"])
if uploaded_file is not None:
    if st.button("Upload & Index Document →", type="primary"):
        with st.spinner("Processing and chunking document into Vector Store..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            url = f"http://localhost:8000/api/v1/projects/{selected_project_id}/documents"
            r = requests.post(url, headers=headers, files=files)
            
            if r.status_code == 200:
                st.success("Document successfully indexed into FAISS Vector Store!")
            else:
                st.error(f"Failed to upload document: {r.text}")
