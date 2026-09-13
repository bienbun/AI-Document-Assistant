import numpy as np
from app.embeddings import get_embedding


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def find_relevant_chunks(question, chunks):
    question_embedding = get_embedding(question)

    scored_chunks = []

    for chunk in chunks:
        chunk_embedding = get_embedding(chunk)

        score = cosine_similarity(
            question_embedding,
            chunk_embedding
        )

        scored_chunks.append((score, chunk))

    scored_chunks.sort(
        reverse=True,
        key=lambda item: item[0]
    )

    return [
        chunk
        for score, chunk in scored_chunks[:3]
    ]