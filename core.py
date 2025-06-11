import os
import shutil
import subprocess
import zipfile
import ffmpeg
import sys


# Convert video file -> WAV audio 
def extract_audio(video_path, audio_output_path):
    ffmpeg.input(video_path).output(audio_output_path, acodec="pcm_s16le", ac=2, ar="44100").run(overwrite_output=True)


# Save uploaded files to disk so external tools can read from it 
def handle_file_upload(uploaded_file, file_path):
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    ext = os.path.splitext(uploaded_file.name)[1].lower()
    audio_path = "converted_audio.wav" if ext in ['.mp4', '.mov'] else file_path

    if ext in ['.mp4', '.mov']:
        extract_audio(file_path, audio_path)
    return audio_path


# Separate audio file -> stems using Demucs
def separate_audio(input_audio_path, output_folder):
    model_name = "htdemucs_6s"
    cmd = [sys.executable, "-m", "demucs","--name", model_name,"--out", output_folder, input_audio_path]

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Demucs ran successfully.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Demucs failed!")
        print("STDOUT:\n", e.stdout)
        print("STDERR:\n", e.stderr)
        raise RuntimeError("Demucs separation failed.")


# Create ZIP file to put all .wav stems in a folder
def zip_stems(stem_folder, zip_path):
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for root, _, files in os.walk(stem_folder):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, stem_folder)
                zipf.write(full_path, arcname)


# Full pipeline of above functions
def run_audio_pipeline(input_audio_path, uploaded_name):
    output_folder = "output_audio"
    model_name = "htdemucs_6s"

    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder, exist_ok=True)

    separate_audio(input_audio_path, output_folder)

    model_output_dir = os.path.join(output_folder, model_name)
    if not os.path.exists(model_output_dir):
        raise FileNotFoundError(f"Expected model output folder not found: {model_output_dir}")

    subfolders = os.listdir(model_output_dir)
    if not subfolders:
        raise FileNotFoundError("No separated stem folders found.")

    stem_folder = os.path.join(model_output_dir, subfolders[0])
    zip_path = f"{stem_folder}.zip"
    zip_stems(stem_folder, zip_path)

    return stem_folder, zip_path
