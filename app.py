import streamlit as st
from core import handle_file_upload, run_audio_pipeline
from ui import show_title_and_uploader, show_results

def main():
    uploaded_file, file_path = show_title_and_uploader()

    if uploaded_file:
        if st.button("Separate Audio"):
            with st.spinner("Separating audio, please wait."):
                input_audio_path = handle_file_upload(uploaded_file, file_path)
                stem_folder, zip_path = run_audio_pipeline(input_audio_path, uploaded_file.name)

                st.session_state.stem_folder = stem_folder
                st.session_state.zip_path = zip_path
                show_results(stem_folder, zip_path)

if __name__ == "__main__":
    main()