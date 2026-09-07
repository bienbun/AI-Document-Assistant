def find_relevant_chunks(question, chunks):
    question_words = set(question.lower().split())

    scored_chunks = []

    for chunk in chunks:
        chunk_words = set(chunk.lower().split())

        score = len(question_words.intersection(chunk_words))

        scored_chunks.append((score, chunk))

    scored_chunks.sort(reverse=True, key=lambda item: item[0])

    return [chunk for score, chunk in scored_chunks[:3] if score > 0]