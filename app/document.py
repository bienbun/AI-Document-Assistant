import re


def clean_text(text):
    # Replace repeated spaces, tabs, and line breaks with one space
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))

        chunk = text[start:end]
        chunks.append(chunk)

        # Stop if this chunk already reached the end of the text
        if end == len(text):
            break

        start += chunk_size - overlap


    return chunks


def chunk_pages(pages, chunk_size=1000, overlap=200):
    chunks = []
    chunk_id = 1

    for page_number, page_text in enumerate(pages, start=1):
        cleaned_text = clean_text(page_text)

        page_chunks = chunk_text(
            cleaned_text,
            chunk_size,
            overlap
        )

        for chunk in page_chunks:
            chunks.append({
                "chunk_id": chunk_id,
                "page": page_number,
                "text": chunk
            })

            chunk_id += 1

    return chunks