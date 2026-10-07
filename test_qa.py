from rag.document_loader import load_documents
from rag.chunking import chunk_documents
from rag.embeddings import embedding_model, create_embeddings
from rag.retriever import retrieve_documents
from rag.qa import generate_answer


print("STEP 1: Loading documents")

documents = load_documents()

print("STEP 2: Creating chunks")

chunks = chunk_documents(documents)

print("STEP 3: Creating embeddings")

embeddings = create_embeddings(chunks)

print("STEP 4: Creating query embedding")

query_embedding = embedding_model.encode(
    "What are the major stages of construction?"
)

print("STEP 5: Retrieving documents")

retrieved_chunks = retrieve_documents(
    query_embedding=query_embedding,
    embeddings=embeddings,
    chunks=chunks,
    top_k=3
)

print("STEP 6: Retrieved documents successfully")

print("STEP 7: Calling Gemini")

answer = generate_answer(
    question="What are the major stages of construction?",
    retrieved_chunks=retrieved_chunks
)

print("STEP 8: Gemini response received")

print("\n==============================")
print("RAG FINAL ANSWER")
print("==============================")
print(answer)