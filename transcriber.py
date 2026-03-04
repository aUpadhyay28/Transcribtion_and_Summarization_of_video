import subprocess
import whisper
import os


def extract_audio(video_path: str, audio_path: str = "temp_audio.wav") -> str:

    if not os.path.exists(video_path):
        raise FileNotFoundError(f"{video_path} not found.")

    if os.path.exists(audio_path):
        os.remove(audio_path)

    command = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        audio_path
    ]

    subprocess.run(command, check=True)

    return audio_path


# Load Whisper model once 
whisper_model = whisper.load_model("base")

def transcribe_audio(audio_path: str) -> str:

    result = whisper_model.transcribe(audio_path)
    return result["text"]
