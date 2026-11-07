import json
import os
from datetime import date, timedelta
from pathlib import Path

import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
SEED_FILE = Path("data/progress.seed.json")

GOAL_STATUSES = ("not_started", "in_progress", "done")
NEW_FEEDBACK_DAYS = 7
UP_NEXT_COUNT = 3


def create_tables(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id          SERIAL PRIMARY KEY,
            user_email  TEXT NOT NULL REFERENCES users(email) ON DELETE CASCADE,
            phase       INTEGER NOT NULL CHECK (phase IN (30, 60, 90)),
            title       TEXT NOT NULL,
            status      TEXT NOT NULL DEFAULT 'not_started'
                        CHECK (status IN ('not_started', 'in_progress', 'done')),
            due_date    DATE,
            position    INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS checklist_items (
            id          SERIAL PRIMARY KEY,
            user_email  TEXT NOT NULL REFERENCES users(email) ON DELETE CASCADE,
            title       TEXT NOT NULL,
            done        BOOLEAN NOT NULL DEFAULT FALSE,
            due_date    DATE,
            position    INTEGER NOT NULL DEFAULT 0
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id          SERIAL PRIMARY KEY,
            user_email  TEXT NOT NULL REFERENCES users(email) ON DELETE CASCADE,
            from_email  TEXT NOT NULL REFERENCES users(email),
            text        TEXT NOT NULL,
            given_on    DATE NOT NULL
        )
    """)
    # One cached AI summary per user, reused until their goals or checklist change.
    conn.execute("""
        CREATE TABLE IF NOT EXISTS summaries (
            user_email   TEXT PRIMARY KEY REFERENCES users(email) ON DELETE CASCADE,
            fingerprint  TEXT NOT NULL,
            summary      JSONB NOT NULL,
            created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)
    for table in ("goals", "checklist_items", "feedback"):
        conn.execute(f"CREATE INDEX IF NOT EXISTS {table}_user_idx ON {table} (user_email)")
    conn.commit()


def seed(conn):
    """Replace every demo user's progress with the sample data."""
    data = json.loads(SEED_FILE.read_text(encoding="utf-8"))
    today = date.today()

    def offset(days):
        return None if days is None else today + timedelta(days=days)

    users = conn.execute("SELECT email, department FROM users").fetchall()
    for email, department in users:
        template = data["departments"].get(department)
        person = data["users"].get(email)
        if template is None or person is None:
            continue

        for table in ("goals", "checklist_items", "feedback", "summaries"):
            conn.execute(f"DELETE FROM {table} WHERE user_email = %s", (email,))

        # The first goals_done goals are done, the next goals_in_progress are underway.
        done, in_progress = person["goals_done"], person["goals_in_progress"]
        for i, goal in enumerate(template["goals"]):
            status = "done" if i < done else "in_progress" if i < done + in_progress else "not_started"
            conn.execute(
                "INSERT INTO goals (user_email, phase, title, status, due_date, position)"
                " VALUES (%s, %s, %s, %s, %s, %s)",
                (email, goal["phase"], goal["title"], status, offset(goal.get("due_in_days")), i),
            )

        for i, item in enumerate(template["checklist"]):
            conn.execute(
                "INSERT INTO checklist_items (user_email, title, done, due_date, position)"
                " VALUES (%s, %s, %s, %s, %s)",
                (email, item["title"], i < person["checklist_done"],
                 offset(item.get("due_in_days")), i),
            )

        for note in person["feedback"]:
            conn.execute(
                "INSERT INTO feedback (user_email, from_email, text, given_on)"
                " VALUES (%s, %s, %s, %s)",
                (email, note["from"], note["text"], offset(-note["days_ago"])),
            )

    conn.commit()
    return len(users)


def current_phase(days_at_nimbus):
    if days_at_nimbus <= 30:
        return 30
    if days_at_nimbus <= 60:
        return 60
    return 90


def get_goals(conn, email):
    rows = conn.execute(
        "SELECT id, phase, title, status, due_date FROM goals"
        " WHERE user_email = %s ORDER BY phase, position, id",
        (email,),
    ).fetchall()
    return [dict(zip(("id", "phase", "title", "status", "due_date"), r)) for r in rows]


def get_checklist(conn, email):
    rows = conn.execute(
        "SELECT id, title, done, due_date FROM checklist_items"
        " WHERE user_email = %s ORDER BY position, id",
        (email,),
    ).fetchall()
    return [dict(zip(("id", "title", "done", "due_date"), r)) for r in rows]


def get_feedback(conn, email):
    rows = conn.execute(
        """
        SELECT f.id, f.from_email, u.name, f.text, f.given_on
        FROM feedback f JOIN users u ON u.email = f.from_email
        WHERE f.user_email = %s
        ORDER BY f.given_on DESC, f.id DESC
        """,
        (email,),
    ).fetchall()
    today = date.today()
    return [
        {"id": id_, "from_email": from_email, "from_name": name, "text": text,
         "date": given_on, "is_new": (today - given_on).days <= NEW_FEEDBACK_DAYS}
        for id_, from_email, name, text, given_on in rows
    ]


def up_next(goals, checklist):
    """The unfinished goals and checklist items due soonest."""
    items = [
        {"kind": "goal", "id": g["id"], "title": g["title"], "phase": g["phase"],
         "status": g["status"], "due_date": g["due_date"]}
        for g in goals if g["status"] != "done"
    ] + [
        {"kind": "checklist", "id": c["id"], "title": c["title"], "due_date": c["due_date"]}
        for c in checklist if not c["done"]
    ]
    items.sort(key=lambda i: (i["due_date"] is None, i["due_date"] or date.max))
    return items[:UP_NEXT_COUNT]


def toggle_checklist_item(conn, email, item_id):
    """Flip one of this user's checklist items. None if it isn't theirs or doesn't exist."""
    row = conn.execute(
        "UPDATE checklist_items SET done = NOT done"
        " WHERE id = %s AND user_email = %s RETURNING id, title, done, due_date",
        (item_id, email),
    ).fetchone()
    conn.commit()
    return dict(zip(("id", "title", "done", "due_date"), row)) if row else None


def set_goal_status(conn, email, goal_id, status):
    """Set one of this user's goals. None if it isn't theirs or doesn't exist."""
    if status not in GOAL_STATUSES:
        raise ValueError(f"unknown status {status!r}")
    row = conn.execute(
        "UPDATE goals SET status = %s"
        " WHERE id = %s AND user_email = %s RETURNING id, phase, title, status, due_date",
        (status, goal_id, email),
    ).fetchone()
    conn.commit()
    return dict(zip(("id", "phase", "title", "status", "due_date"), row)) if row else None


if __name__ == "__main__":
    with psycopg.connect(DATABASE_URL) as conn:
        create_tables(conn)
        count = seed(conn)
        print(f"seeded progress for {count} users\n")

        rows = conn.execute("""
            SELECT u.email,
                   (SELECT count(*) FROM goals g WHERE g.user_email = u.email),
                   (SELECT count(*) FROM checklist_items c WHERE c.user_email = u.email),
                   (SELECT count(*) FROM feedback f WHERE f.user_email = u.email)
            FROM users u ORDER BY u.department, u.email
        """).fetchall()
        for email, goals, items, notes in rows:
            print(f"  {email:<24} {goals} goals  {items} checklist  {notes} feedback")
