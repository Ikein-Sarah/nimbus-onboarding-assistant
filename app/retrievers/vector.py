import os
from dotenv import load_dotenv
import psycopg
from openai import OpenAI

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
MODEL = "text-embedding-3-small"
TOP_K = 5

client = OpenAI()


def embed_question(question):
    response = client.embeddings.create(model=MODEL, input=[question])
    return response.data[0].embedding


def retrieve(question, email, department, top_k=TOP_K):
    vector = embed_question(question)

    with psycopg.connect(DATABASE_URL) as conn:
        rows = conn.execute(
            """
            SELECT text, path, department, owner, embedding <=> %s AS distance
            FROM chunks
            WHERE department IN ('general', %s)
              AND owner IN ('all', %s)
            ORDER BY distance
            LIMIT %s
            """,
            (str(vector), department, email, top_k),
        ).fetchall()

    return [
        {"text": r[0], "path": r[1], "department": r[2],
         "owner": r[3], "distance": r[4]}
        for r in rows
    ]


if __name__ == "__main__":
    question = "What is the pay band for a senior engineer?"

    people = [
        ("tunde@nimbuslabs.io", "people"),
        ("sarah@nimbuslabs.io", "engineering"),
    ]

    for email, dept in people:
        print(f"\n=== {email} ({dept}) ===")
        results = retrieve(question, email, dept)
        for r in results:
            print(f"{r['distance']:.3f}  {r['path']}")
            print(f"        {r['text'][:90]}...")