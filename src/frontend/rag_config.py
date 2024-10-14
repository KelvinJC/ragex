import streamlit as st
from speech_to_text import recognise_speech


selected_project_id = None
selected_project = None

def get_configs():
    with st.sidebar:
        with st.form("🗀 File Input", clear_on_submit=True):
            uploaded_files = st.file_uploader(
                "Upload local files:",
                type=["txt", "pdf", "docx", "csv", "jpg", "png", "jpeg", "py"],
                accept_multiple_files=True,
            )
            submitted = st.form_submit_button("Submit")
        if uploaded_files and submitted:
            st.session_state["uploaded_files"] = uploaded_files

        record_section = st.expander("🗀 Records", expanded=True)
        with record_section:    
            audio_value = st.experimental_audio_input("Voice chat")
            if audio_value:
                st.audio(audio_value)
                st.session_state["audio_to_text"] = recognise_speech(file=audio_value)

        project_section = st.expander("🗀 Projects", expanded=True)
        with project_section:
            last_submitted_embeddings = (len(st.session_state["projects"]) - 1) if st.session_state["projects"] else None
            selected_project = st.selectbox(
                "Select embeddings for chat: ", 
                st.session_state["projects"], 
                on_change=change_id, 
                index=last_submitted_embeddings,
            )
        model_section = st.expander("🗄 Models", expanded=True)
        with model_section:
            selected_model = st.selectbox("Select your preferred model: ", [
                "llama-3.1-70b-versatile",
                "llama-3.1-8b-instant",
                "mixtral-8x7b-32768"
            ])
        # select rag parameters
        rag_section = st.expander("⚒ RAG Configuration", expanded=True)
        with rag_section:
            max_tokens = st.number_input("Max Tokens", min_value=1, max_value=1024, value=512)
            temperature = st.slider("Temperature", min_value=0.01, max_value=2.0, value=0.0, step=0.01, format="%.1f")

        vars = (selected_model, temperature, submitted, max_tokens, selected_project)
        return vars 

def change_id():
    selected_project_id = selected_project