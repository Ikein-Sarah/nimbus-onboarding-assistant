from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.documents import load_documents

splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=150)


def chunk_documents(docs):
    chunks = []
    for doc in docs:
        for piece in splitter.split_text(doc["text"]):
            chunks.append({
                "text": piece,
                "path": doc["path"],
                "department": doc["department"],
                "owner": doc["owner"],
            })
    return chunks


if __name__ == "__main__":
    docs = load_documents()
    chunks = chunk_documents(docs)

    print(f"{len(docs)} documents -> {len(chunks)} chunks")
    lengths = [len(c["text"]) for c in chunks]
    print(f"average {sum(lengths) // len(lengths)} characters")

    sample = chunks[len(chunks) // 2]
    print("\n--- one chunk ---")
    print(sample["path"], "|", sample["department"], "|", sample["owner"])
    print(sample["text"][:400])