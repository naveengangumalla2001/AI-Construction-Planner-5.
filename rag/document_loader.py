from pathlib import Path


def load_documents():
    documents_path = Path("rag/documents")

    documents = []

    for file_path in documents_path.glob("*.txt"):

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        documents.append({
            "source": file_path.name,
            "content": content
        })

    return documents