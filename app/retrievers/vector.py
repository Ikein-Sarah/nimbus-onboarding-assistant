import os
from dotenv import load_dotenv
import psycopg
from openai import OpenAI

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
MODEL = "text-embedding-3-small"
TOP_K = 5
CANDIDATES = 20
RRF_K = 60

client = OpenAI()


def embed_question(question):
    response = client.embeddings.create(model=MODEL, input=[question])
    return response.data[0].embedding


def rank_dense(conn, vector, email, department):
    rows = conn.execute(
        """
        SELECT id FROM chunks
        WHERE department IN ('general', %s)
          AND owner IN ('all', %s)
        ORDER BY embedding <=> %s
        LIMIT %s
        """,
        (department, email, str(vector), CANDIDATES),
    ).fetchall()
    return [r[0] for r in rows]


def rank_sparse(conn, question, email, department):
    rows = conn.execute(
        """
        SELECT id FROM chunks
        WHERE department IN ('general', %s)
          AND owner IN ('all', %s)
          AND tsv @@ replace(plainto_tsquery('english', %s)::text, '&', '|')::tsquery
        ORDER BY ts_rank(tsv, replace(plainto_tsquery('english', %s)::text, '&', '|')::tsquery) DESC
        LIMIT %s
        """,
        (department, email, question, question, CANDIDATES),
    ).fetchall()
    return [r[0] for r in rows]


def fuse(dense_ids, sparse_ids):
    scores = {}
    for ids in (dense_ids, sparse_ids):
        for position, chunk_id in enumerate(ids, start=1):
            scores[chunk_id] = scores.get(chunk_id, 0) + 1 / (RRF_K + position)
    return sorted(scores, key=scores.get, reverse=True)


def retrieve(question, email, department, top_k=TOP_K):
    vector = embed_question(question)

    with psycopg.connect(DATABASE_URL) as conn:
        dense_ids = rank_dense(conn, vector, email, department)
        sparse_ids = rank_sparse(conn, question, email, department)

        best_ids = fuse(dense_ids, sparse_ids)[:top_k]
        if not best_ids:
            return []

        rows = conn.execute(
            "SELECT id, text, path, department, owner FROM chunks WHERE id = ANY(%s)",
            (best_ids,),
        ).fetchall()

    by_id = {r[0]: r for r in rows}
    return [
        {"text": by_id[i][1], "path": by_id[i][2],
         "department": by_id[i][3], "owner": by_id[i][4]}
        for i in best_ids if i in by_id
    ]

if __name__ == "__main__":
    question = "What does the PR checklist require before merge?"

    with psycopg.connect(DATABASE_URL) as conn:
        vector = embed_question(question)
        print("dense ids: ", rank_dense(conn, vector, "sarah@nimbuslabs.io", "engineering"))
        print("sparse ids:", rank_sparse(conn, question, "sarah@nimbuslabs.io", "engineering"))

    print("\n=== fused result ===")
    for r in retrieve(question, "sarah@nimbuslabs.io", "engineering"):
        print(r["path"])
        print(f"        {r['text'][:90]}...")