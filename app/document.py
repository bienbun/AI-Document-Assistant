import re


def clean_text(text):
    # Replace repeated spaces, tabs, and line breaks with one space
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks