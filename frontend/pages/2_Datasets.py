import streamlit as st
import pandas as pd
from utils.auth import init_session, is_authenticated
from utils.api import api_get, api_post_file, api_delete

st.set_page_config(page_title="Datasets", page_icon="📊")

init_session()

if not is_authenticated():
    st.warning("Please log in from the main page to access Datasets.")
    st.stop()

st.title("📊 Datasets")

# Fetch projects for dropdown
resp = api_get("/projects/", token=st.session_state.token)
if resp.status_code != 200:
    st.error("Failed to fetch projects.")
    st.stop()

projects = resp.json()
if not projects:
    st.info("You need to create a Project first before uploading datasets.")
    st.stop()

project_map = {p['name']: p['id'] for p in projects}
selected_project_name = st.selectbox("Select Project", options=list(project_map.keys()))
selected_project_id = project_map[selected_project_name]

st.divider()

# Upload Dataset
st.subheader("Upload New Dataset")
with st.form("upload_dataset_form", clear_on_submit=True):
    d_name = st.text_input("Dataset Name (required)")
    d_desc = st.text_area("Description (optional)")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    
    submit_upload = st.form_submit_button("Upload")
    if submit_upload:
        if not d_name or not uploaded_file:
            st.error("Dataset Name and File are required.")
        else:
            files = {"file": (uploaded_file.name, uploaded_file, "text/csv")}
            data = {"name": d_name, "description": d_desc or ""}
            
            with st.spinner("Uploading..."):
                up_resp = api_post_file(f"/projects/{selected_project_id}/datasets", files=files, data=data, token=st.session_state.token)
            
            if up_resp.status_code == 200:
                st.success("Dataset uploaded successfully!")
                st.rerun()
            else:
                st.error(f"Upload failed: {up_resp.text}")

st.divider()

# List Datasets
st.subheader("Project Datasets")
ds_resp = api_get(f"/projects/{selected_project_id}/datasets", token=st.session_state.token)
if ds_resp.status_code == 200:
    datasets = ds_resp.json()
    if not datasets:
        st.info("No datasets found for this project.")
    else:
        # Prepare dataframe for nice display
        df_data = []
        for d in datasets:
            df_data.append({
                "Name": d["name"],
                "Description": d["description"],
                "Size (KB)": round(d["file_size"] / 1024, 2),
                "Uploaded At": d["uploaded_at"][:19],
                "ID": d["id"]
            })
        
        st.dataframe(pd.DataFrame(df_data), use_container_width=True)
        
        # Deletion controls
        st.write("---")
        st.write("**Manage Datasets**")
        del_col1, del_col2 = st.columns([3, 1])
        with del_col1:
            dataset_to_delete = st.selectbox("Select dataset to delete", options=[d["name"] for d in datasets])
        with del_col2:
            st.write("") # Spacer
            st.write("") # Spacer
            if st.button("Delete Selected Dataset", type="primary"):
                del_id = next(d["id"] for d in datasets if d["name"] == dataset_to_delete)
                del_resp = api_delete(f"/projects/{selected_project_id}/datasets/{del_id}", token=st.session_state.token)
                if del_resp.status_code == 200:
                    st.success("Dataset deleted!")
                    st.rerun()
                else:
                    st.error("Failed to delete dataset.")
else:
    st.error("Failed to fetch datasets.")
