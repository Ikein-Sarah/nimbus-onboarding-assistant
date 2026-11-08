"""Usage limits that protect the OpenAI budget of the public demo.

Counts live in Postgres rather than in memory, because the free Render server
restarts whenever it wakes from sleep and in-memory counts would reset.
"""

import psycopg

ASK_PER_HOUR = 10
ASK_PER_DAY = 30
OPENAI_CALLS_PER_DAY = 200

# One question is two OpenAI calls: embedding the question, then the answer.
CALLS_PER_QUESTION = 2

LIMIT_MESSAGE = "This demo has a daily question limit. Please try again tomorrow."


def create_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS usage_counts (
            key           TEXT NOT NULL,
            window_start  TIMESTAMPTZ NOT NULL,
            count         INTEGER NOT NULL,
            PRIMARY KEY (key, window_start)
        )
    """)
    conn.commit()


def _take(conn, key, window, amount, limit):
    """Add amount to the count for this window, unless that would pass the limit."""
    row = conn.execute(
        """
        INSERT INTO usage_counts (key, window_start, count)
        VALUES (%(key)s, date_trunc(%(window)s, now(), 'UTC'), %(amount)s)
        ON CONFLICT (key, window_start) DO UPDATE
            SET count = usage_counts.count + EXCLUDED.count
            WHERE usage_counts.count + EXCLUDED.count <= %(limit)s
        RETURNING count
        """,
        {"key": key, "window": window, "amount": amount, "limit": limit},
    ).fetchone()
    return row is not None


def _take_all(conn, rules):
    """Take from every counter, or from none of them if any is used up.

    Windows are in UTC, so the daily limits reset at midnight UTC.
    """
    allowed = False
    with conn.transaction():
        conn.execute("DELETE FROM usage_counts WHERE window_start < now() - interval '2 days'")
        if not all(_take(conn, *rule) for rule in rules):
            raise psycopg.Rollback()
        allowed = True
    conn.commit()
    return allowed


def allow_question(conn, ip_key):
    """Count one question from this address. False if a limit has been reached."""
    return _take_all(conn, [
        (f"ask-hour:{ip_key}", "hour", 1, ASK_PER_HOUR),
        (f"ask-day:{ip_key}", "day", 1, ASK_PER_DAY),
        ("openai", "day", CALLS_PER_QUESTION, OPENAI_CALLS_PER_DAY),
    ])


def allow_openai_call(conn):
    """Count one OpenAI call against the app-wide daily cap."""
    return _take_all(conn, [("openai", "day", 1, OPENAI_CALLS_PER_DAY)])
