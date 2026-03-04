import re


def chunk_text(text: str, chunk_size: int = 2000, overlap: int = 200) -> list:
    """
    Splits text into chunks of approximately `chunk_size` characters,
    with optional overlap to preserve context.

    :param text: Full text input
    :param chunk_size: Maximum characters per chunk
    :param overlap: Overlapping characters between chunks
    :return: List of text chunks
    """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunks.append(text[start:end])

        start += chunk_size - overlap

        if start < 0:
            start = 0

    return chunks


def chunked_summarize(text: str, summarize_func, max_chunk_size: int = 2000) -> str:
    """
    Summarizes large text by:
    1. Splitting into chunks
    2. Summarizing each chunk
    3. Combining summaries
    4. Running a final summarization

    :param text: Full text to summarize
    :param summarize_func: Function that returns summary of text
    :param max_chunk_size: Maximum characters per chunk
    :return: Final summary
    """

    # 1️⃣ Split text
    text_chunks = chunk_text(text, chunk_size=max_chunk_size, overlap=200)

    # 2️⃣ Summarize each chunk
    partial_summaries = [summarize_func(chunk) for chunk in text_chunks]

    # 3️⃣ Combine
    combined_text = " ".join(partial_summaries)

    # 4️⃣ Final summarization
    final_summary = summarize_func(combined_text)

    return final_summary


def contains_blocked_words(text: str, blocked_words: set) -> bool:
    """
    Checks if text contains any blocked words or phrases.

    :param text: Input text
    :param blocked_words: Set of blocked keywords
    :return: True if restricted word found
    """
    text = text.lower()

    for phrase in blocked_words:
        # Match whole words only
        pattern = r"\b" + re.escape(phrase.lower()) + r"\b"

        if re.search(pattern, text):
            return True

    return False