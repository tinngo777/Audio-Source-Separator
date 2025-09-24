import os
import streamlit as st
import uuid
import numpy as np

def show_title_and_uploader():
    st.title("TN Audio Player and Separator")
    uploaded_file = st.file_uploader("Upload your audio", type=['mp3', 'wav', 'mp4', 'mov'])
    if uploaded_file:
        st.success("File uploaded successfully.")
        file_path = f"{uploaded_file.name}"
        return uploaded_file, file_path
    return None, None

def show_audio_controls(input_audio_path):
    audio_file = open(input_audio_path, "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/ogg")


def show_results(stem_folder, zip_path):
    st.success("Audio separated successfully!")

    if zip_path and os.path.exists(zip_path):
        with open(zip_path, "rb") as f:
            unique_id = uuid.uuid4().hex  
            st.download_button(
                label="Download ZIP",
                data=f,
                file_name=os.path.basename(zip_path),
                key=f"download_zip_{unique_id}"
            )
    
    st.info("To separate another file, please refresh the page.")
