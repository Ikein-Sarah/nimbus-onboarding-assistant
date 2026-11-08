"""One-time database setup: pgvector, every table, demo data and embeddings.

Run it once from your laptop against the hosted database:

    DATABASE_URL='<Neon connection string>' python -m scripts.setup_db

OPENAI_API_KEY and DEMO_PASSWORD are read from .env. A DATABASE_URL given on
the command line wins over the one in .env. Running it again resets the demo
data and re-embeds the documents.
"""

import os
from urllib.parse import urlsplit

import psycopg

from app import embed, limits, progress, users
from app.chunking import chunk_documents
from app.db import DATABASE_URL
from app.documents import load_documents


def main():
    password = os.environ.get("DEMO_PASSWORD")
    if not password:
        raise SystemExit("Set DEMO_PASSWORD in .env first.")

    print(f"Setting up the database at {urlsplit(DATABASE_URL).hostname}\n")

    with psycopg.connect(DATABASE_URL) as conn:
        conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        conn.commit()
        print("pgvector enabled")

        users.create_table(conn)
        print(f"seeded {users.seed(conn, password)} users")

        progress.create_tables(conn)
        print(f"seeded progress for {progress.seed(conn)} users")

        limits.create_table(conn)
        print("usage limits table ready")

        chunks = chunk_documents(load_documents())
        print(f"embedding {len(chunks)} chunks")
        embed.create_table(conn)
        embed.store(conn, chunks)

        count = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
        print(f"\ndone, {count} chunks stored")


if __name__ == "__main__":
    main()
