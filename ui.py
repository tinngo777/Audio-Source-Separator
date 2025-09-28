import os
import streamlit as st
import uuid
import streamlit.components.v1 as components
import urllib.parse
import base64
import time

def show_title_and_uploader():
    st.title("TN Audio Player and Separator")
    uploaded_file = st.file_uploader("Upload your audio", type=['mp3', 'wav', 'mp4', 'mov'])
    msg = st.empty()
    if uploaded_file:
        msg.success("File uploaded successfully.")
        time.sleep(2)
        msg.empty()
        
        file_path = f"{uploaded_file.name}"
        return uploaded_file, file_path
    return None, None

def show_audio_player_ui(file_path):
    # Read and encode audio file as base64
    with open(file_path, "rb") as f:
        audio_bytes = f.read()
    base64_audio = base64.b64encode(audio_bytes).decode()

    html_string = f"""
    <div style="background-color:#0e1117;padding:20px;border-radius:10px">
      <h3 style="color:white;"><i>Audio Player</i></h3>
      <div id="waveform"></div>

      <div style="margin-top:5px;">
        <button onclick="wavesurfer.play()">▶</button>
        <button onclick="wavesurfer.pause()">⏸</button>
        <button onclick="wavesurfer.stop()">⏹ Stop</button>
        <label style="color:white;margin-left:10px;">Volume:</label>
        <input type="range" min="0" max="1" step="0.01" value="1" onchange="wavesurfer.setVolume(this.value)" style="vertical-align:middle;">
      </div>
    </div>

    <script src="https://unpkg.com/wavesurfer.js"></script>
    <script>
    const wavesurfer = WaveSurfer.create({{
        container: '#waveform',
        waveColor: '#4b8bbe',
        progressColor: '#1E88E5',
        cursorColor: '#fff',
        barWidth: 2,
        height: 120,
        responsive: true
    }});

    const audioData = "data:audio/mp3;base64,{base64_audio}";
    wavesurfer.load(audioData);
    </script>
    """

    components.html(html_string, height=360, scrolling=True)

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
