import json
import os
from pathlib import Path

import bcrypt
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
SEED_FILE = Path("data/users.seed.json")


def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def check_password(password, password_hash):
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except ValueError:
        # bcrypt rejects passwords over 72 bytes. Treat that as a wrong password.
        return False


USER_FIELDS = ("email", "name", "department", "title", "start_date", "manager_email",
               "password_hash")


def get_user(conn, email):
    row = conn.execute(
        f"SELECT {', '.join(USER_FIELDS)} FROM users WHERE email = %s",
        (email,),
    ).fetchone()
    if row is None:
        return None
    return dict(zip(USER_FIELDS, row))


def create_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email          TEXT PRIMARY KEY,
            name           TEXT NOT NULL,
            department     TEXT NOT NULL,
            title          TEXT NOT NULL,
            password_hash  TEXT NOT NULL
        )
    """)
    # Added after the table first shipped, so older databases get them too.
    conn.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS start_date DATE")
    conn.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS manager_email TEXT")
    conn.commit()


def seed(conn, password):
    users = json.loads(SEED_FILE.read_text(encoding="utf-8"))

    for user in users:
        # The seed file calls the department "role".
        conn.execute(
            """
            INSERT INTO users (email, name, department, title, start_date, password_hash)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (email) DO UPDATE SET
                name = EXCLUDED.name,
                department = EXCLUDED.department,
                title = EXCLUDED.title,
                start_date = EXCLUDED.start_date,
                password_hash = EXCLUDED.password_hash
            """,
            (user["email"], user["name"], user["role"], user["title"],
             user["start_date"], hash_password(password)),
        )

    # Managers are set in a second pass, once every user row exists.
    for user in users:
        conn.execute("UPDATE users SET manager_email = %s WHERE email = %s",
                     (user["manager_email"], user["email"]))

    conn.commit()
    return len(users)


if __name__ == "__main__":
    password = os.environ.get("DEMO_PASSWORD")
    if not password:
        raise SystemExit("Set DEMO_PASSWORD in .env before seeding users.")

    with psycopg.connect(DATABASE_URL) as conn:
        create_table(conn)
        count = seed(conn, password)
        print(f"seeded {count} users\n")

        rows = conn.execute(
            "SELECT email, department, title FROM users ORDER BY department, email"
        ).fetchall()
        for email, department, title in rows:
            print(f"  {department:<12} {email:<24} {title}")
