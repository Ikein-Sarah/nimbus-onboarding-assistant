import hashlib
import json
import logging
from datetime import date

from dotenv import load_dotenv
from openai import OpenAI
from psycopg.types.json import Jsonb

load_dotenv()

MODEL = "gpt-4o"
TAGS = ("Done", "Soon", "Next")

client = OpenAI()
log = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You write a short weekly progress summary for a new employee at Nimbus Labs,
from their onboarding goals and checklist.

Rules:

1. Write to the employee, in the second person ("You finished...", "Your
   on-call shadow is on Friday"). Warm and plain, like a helpful colleague.

2. overview: one sentence on how they're doing overall, under 20 words.

3. items: exactly 3 short items, each under 12 words, each tagged:
   - Done: something they have finished
   - Soon: something unfinished that is due in the next 7 days
   - Next: what they should focus on after that
   Use one of each tag when the data allows it. If nothing fits a tag, use
   another tag rather than inventing work.

4. Only mention goals and checklist items that appear in the data. Do not
   invent dates, people or tasks. Refer to dates relative to today, such as
   "on Friday" or "next week".
"""

SCHEMA = {
    "type": "object",
    "properties": {
        "overview": {"type": "string"},
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "tag": {"type": "string", "enum": list(TAGS)},
                    "text": {"type": "string"},
                },
                "required": ["tag", "text"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["overview", "items"],
    "additionalProperties": False,
}


def describe(goals, checklist, start_date, today):
    lines = [f"Today: {today:%A %d %B %Y}", f"Started at Nimbus: {start_date:%d %B %Y}", "",
             "Goals:"]
    for g in goals:
        due = f", due {g['due_date']:%A %d %B}" if g["due_date"] else ""
        lines.append(f"- [{g['phase']}-day] {g['title']}: {g['status'].replace('_', ' ')}{due}")
    lines += ["", "Checklist:"]
    for c in checklist:
        due = f", due {c['due_date']:%A %d %B}" if c["due_date"] else ""
        lines.append(f"- {c['title']}: {'done' if c['done'] else 'not done'}{due}")
    return "\n".join(lines)


def generate(goals, checklist, start_date, today):
    response = client.responses.create(
        model=MODEL,
        instructions=SYSTEM_PROMPT,
        input=describe(goals, checklist, start_date, today),
        text={"format": {"type": "json_schema", "name": "weekly_summary",
                         "schema": SCHEMA, "strict": True}},
    )
    result = json.loads(response.output_text)
    return {"overview": result["overview"].strip(), "items": result["items"][:3]}


def weekly_summary(conn, email, goals, checklist, start_date):
    """The user's summary, regenerated only when their progress or the date changes.

    Returns None if the model call fails, so the dashboard still loads.
    """
    today = date.today()
    fingerprint = hashlib.sha256(
        describe(goals, checklist, start_date, today).encode("utf-8")
    ).hexdigest()

    row = conn.execute(
        "SELECT summary FROM summaries WHERE user_email = %s AND fingerprint = %s",
        (email, fingerprint),
    ).fetchone()
    if row:
        return row[0]

    try:
        summary = generate(goals, checklist, start_date, today)
    except Exception:
        log.exception("weekly summary failed for %s", email)
        return None

    conn.execute(
        """
        INSERT INTO summaries (user_email, fingerprint, summary) VALUES (%s, %s, %s)
        ON CONFLICT (user_email) DO UPDATE SET
            fingerprint = EXCLUDED.fingerprint,
            summary = EXCLUDED.summary,
            created_at = now()
        """,
        (email, fingerprint, Jsonb(summary)),
    )
    conn.commit()
    return summary
