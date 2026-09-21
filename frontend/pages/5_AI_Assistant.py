import streamlit as st
from utils.auth import init_session, is_authenticated
from utils.api import api_post

st.set_page_config(page_title="AI Assistant", page_icon="🤖")
init_session()

if not is_authenticated():
    st.warning("Please log in to chat with the AI Assistant.")
    st.stop()

st.title("🤖 AI Experiment Assistant")
st.caption("Ask me about your projects, experiments, or MLflow runs! (Requires GEMINI_API_KEY in backend .env)")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask something (e.g. 'What projects do I have?'):"):
    # Append user message
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            resp = api_post("/assistant/chat", json={"message": prompt}, token=st.session_state.token)
            if resp.status_code == 200:
                reply = resp.json().get("reply", "No response")
                st.markdown(reply)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
            else:
                st.error("Failed to connect to AI Agent. Is GEMINI_API_KEY set?")
