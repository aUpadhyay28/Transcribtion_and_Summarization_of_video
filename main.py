# main.py

import os
from transcriber import extract_audio, transcribe_audio
from summarizer import summarize_text
from utils import chunked_summarize, contains_blocked_words


def video_to_summary(
    video_path: str,
    use_chunking: bool = True
) -> str:

    # 🔒 Define blocked words / phrases
    BLOCKED_WORDS = {
        "violence",
        "drugs",
        "best",
        "weapon",
        "explicit content",
        "money laundering"
    }

    # 1️⃣ Extract audio
    audio_path = "temp_audio.wav"
    extract_audio(video_path, audio_path)

    # 2️⃣ Transcribe audio
    transcript = transcribe_audio(audio_path)

    # 3️⃣ Strict content filtering
    if contains_blocked_words(transcript, BLOCKED_WORDS):

        if os.path.exists(audio_path):
            os.remove(audio_path)

        return "Summary not generated due to restricted content."

    # 4️⃣ Summarize
    if use_chunking:
        final_summary = chunked_summarize(
            text=transcript,
            summarize_func=summarize_text,
            max_chunk_size=2000
        )
    else:
        final_summary = summarize_text(transcript)

    # 5️⃣ Cleanup
    if os.path.exists(audio_path):
        os.remove(audio_path)

    return final_summary


if __name__ == "__main__":

    video_file = "example_video.mp4"

    summary_output = video_to_summary(video_file)

    print("=== Final Summary ===")
    print(summary_output)