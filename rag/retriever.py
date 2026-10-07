import numpy as np


def retrieve_documents(
    query_embedding,
    embeddings,
    chunks,
    top_k=3
):
    query_embedding = np.array(
        [query_embedding]
    ).astype("float32")

    embeddings = np.array(
        embeddings
    ).astype("float32")

    # Calculate L2 distance
    distances = np.linalg.norm(
        embeddings - query_embedding,
        axis=1
    )

    # Get nearest chunks
    top_indices = np.argsort(distances)[:top_k]

    results = []

    for index in top_indices:
        results.append({
            "content": chunks[index]["content"],
            "source": chunks[index]["source"],
            "distance": float(distances[index])
        })

    return results