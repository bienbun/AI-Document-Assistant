import numpy as np
from app.embeddings import get_embedding


def cosine_similarity(a, b):
    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


def create_chunk_embeddings(chunks):
    return [
        get_embedding(chunk).tolist()
        for chunk in chunks
    ]


def find_relevant_chunks(question, chunks, chunk_embeddings):
    question_embedding = get_embedding(question)

    scored_chunks = []

    for chunk, chunk_embedding in zip(chunks, chunk_embeddings):
        score = cosine_similarity(
            question_embedding,
            np.array(chunk_embedding)
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