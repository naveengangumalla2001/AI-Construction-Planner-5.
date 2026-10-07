def chunk_documents(documents, chunk_size=500, chunk_overlap=50):

    chunks = []

    for document in documents:

        text = document["content"]
        source = document["source"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end]

            chunks.append({
                "content": chunk_text,
                "source": source
            })

            start += chunk_size - chunk_overlap

    return chunks