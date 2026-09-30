import os
from dotenv import load_dotenv
import psycopg
from openai import OpenAI

from app.documents import load_documents
from app.chunking import chunk_documents

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
MODEL = "text-embedding-3-small"
DIMENSIONS = 1536
BATCH_SIZE = 100

client = OpenAI()


def create_table(conn):
    conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
    conn.execute("DROP TABLE IF EXISTS chunks")
    conn.execute(f"""
        CREATE TABLE chunks (
            id          SERIAL PRIMARY KEY,
            text        TEXT NOT NULL,
            path        TEXT NOT NULL,
            department  TEXT NOT NULL,
            owner       TEXT NOT NULL,
            embedding   vector({DIMENSIONS}) NOT NULL
        )
    """)
    conn.commit()


def embed_batch(texts):
    response = client.embeddings.create(model=MODEL, input=texts)
    return [item.embedding for item in response.data]


def store(conn, chunks):
    for start in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[start:start + BATCH_SIZE]
        vectors = embed_batch([c["text"] for c in batch])

        for chunk, vector in zip(batch, vectors):
            conn.execute(
                """
                INSERT INTO chunks (text, path, department, owner, embedding)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (chunk["text"], chunk["path"], chunk["department"],
                 chunk["owner"], str(vector)),
            )

        conn.commit()
        print(f"stored {start + len(batch)} / {len(chunks)}")


if __name__ == "__main__":
    docs = load_documents()
    chunks = chunk_documents(docs)
    print(f"{len(chunks)} chunks to embed")

    with psycopg.connect(DATABASE_URL) as conn:
        create_table(conn)
        store(conn, chunks)

        count = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
        print(f"\ndone, {count} rows in the table")

        rows = conn.execute(
            "SELECT department, COUNT(*) FROM chunks GROUP BY department ORDER BY 2 DESC"
        ).fetchall()
        for dept, n in rows:
            print(f"  {dept}: {n}")