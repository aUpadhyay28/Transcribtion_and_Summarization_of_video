import os
from transcriber import extract_audio, transcribe_audio
from summarizer import summarize_text
from utils import chunked_summarize, contains_blocked_words
from detoxify import Detoxify


# Load Detoxify model once
toxicity_model = Detoxify("original")


# Keyword blacklist (fast filtering)
BLOCKED_WORDS = {
    "violence",
    "drugs",
    "crime",
    "weapon",
    "explicit content",
    "money laundering"
}


def is_toxic(text: str, epsilon: float = 0.01) -> bool:
    """
    Strict toxicity detection.
    Blocks if ANY toxicity score exceeds epsilon (default 1%).
    """
    results = toxicity_model.predict(text)

    print("Toxicity Scores:", results)

    for score in results.values():
        if score > epsilon:
            return True

    return False


def is_restricted(text: str) -> bool:
    """
    Hybrid filtering:
     Keyword filter
     ML toxicity detection
    """

    # Fast keyword check
    if contains_blocked_words(text, BLOCKED_WORDS):
        print("Blocked due to keyword match.")
        return True

    # ML toxicity check
    if is_toxic(text):
        print("Blocked due to ML toxicity detection.")
        return True

    return False


def video_to_summary(video_path: str, use_chunking: bool = True) -> str:

    # Extract audio
    audio_path = "temp_audio.wav"
    extract_audio(video_path, audio_path)

    # Transcribe audio
    transcript = transcribe_audio(audio_path)

    print("\n=== Transcript ===")
    print(transcript)
    print("==================\n")

    # Hybrid Filtering (Chunk-Level Check)
    transcript_chunks = transcript.split(". ")

    for chunk in transcript_chunks:
        if is_restricted(chunk):

            if os.path.exists(audio_path):
                os.remove(audio_path)

            return "Summary not generated due to restricted content."

    #  Summarize (only if safe)
    if use_chunking:
        final_summary = chunked_summarize(
            text=transcript,
            summarize_func=summarize_text,
            max_chunk_size=2000
        )
    else:
        final_summary = summarize_text(transcript)

    #  Cleanup
    if os.path.exists(audio_path):
        os.remove(audio_path)

    return final_summary


if __name__ == "__main__":

    video_file = "example_video.mp4"

    summary_output = video_to_summary(video_file)

    print("\n=== Final Summary ===")
    print(summary_output)