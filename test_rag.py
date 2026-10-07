from rag.document_loader import load_documents
from rag.chunking import chunk_documents
from rag.embeddings import embedding_model, create_embeddings
from rag.retriever import retrieve_documents


# 1. Load documents
documents = load_documents()

print("Documents loaded:", len(documents))


# 2. Create chunks
chunks = chunk_documents(documents)

print("Chunks created:", len(chunks))


# 3. Create embeddings
embeddings = create_embeddings(chunks)

print("Embeddings shape:", embeddings.shape)


# 4. User question
question = "What are the major stages of construction?"


# 5. Convert question into embedding
query_embedding = embedding_model.encode(question)


# 6. Retrieve relevant chunks
results = retrieve_documents(
    query_embedding=query_embedding,
    embeddings=embeddings,
    chunks=chunks,
    top_k=3
)


# 7. Display results
print("\nRetrieved Documents:\n")

for i, result in enumerate(results, start=1):
    print(f"--- Result {i} ---")
    print("Source:", result["source"])
    print("Distance:", result["distance"])
    print("Content:")
    print(result["content"])
    print()