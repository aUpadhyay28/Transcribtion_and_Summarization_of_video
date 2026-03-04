
import os
#os.environ["HF_HUB_OFFLINE"] = "1"

from transformers import pipeline

# Load summarization pipeline (offline from cache)
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

def summarize_text(
    text: str,
    max_length: int = 50,
    min_length: int = 5
) -> str:

    # Skip summarization if text too short
    if len(text.split()) < 40:
        return text

    summary = summarizer(
        text,
        max_length=max_length,
        min_length=min_length,
        do_sample=False
    )

    return summary[0]["summary_text"]