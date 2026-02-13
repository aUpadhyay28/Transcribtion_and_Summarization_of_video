import os
from transcriber import extract_audio, transcribe_audio
from summarizer import summarize_text
from utils import chunked_summarize


def video_to_summary(
    video_path: str,
    model_size: str = "base",
    use_chunking: bool = False
) -> str:

    # 1️⃣ Extract audio
    audio_path = "temp_audio.wav"
    extract_audio(video_path, audio_path)

    # 2️⃣ Transcribe audio
    transcript = transcribe_audio(audio_path, model_size=model_size)

    # 3️⃣ Summarize transcript
    if use_chunking:
        final_summary = chunked_summarize(
            text=transcript,
            summarize_func=lambda txt: summarize_text(txt),
            max_chunk_size=2000
        )
    else:
        final_summary = summarize_text(transcript)

    # 4️⃣ Cleanup temp file
    if os.path.exists(audio_path):
        os.remove(audio_path)

    return final_summary


if __name__ == "__main__":
    video_file = "example_video.mp4"

    summary_output = video_to_summary(
        video_file,
        model_size="base",
        use_chunking=True
    )

    print("=== Final Summary ===")
    print(summary_output)
