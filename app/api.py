import os
import time
from datetime import datetime, timedelta, timezone
from typing import Literal

import jwt
import psycopg
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, ConfigDict, Field

from app import progress
from app.answer import answer
from app.summary import weekly_summary
from app.users import check_password, get_user, hash_password

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
JWT_SECRET = os.environ["JWT_SECRET"]
if len(JWT_SECRET) < 32:
    raise RuntimeError("JWT_SECRET must be at least 32 characters")
JWT_ALGORITHM = "HS256"
TOKEN_HOURS = 4

# Checked when the email is unknown, so a wrong email takes as long as a wrong
# password and the response time doesn't reveal which emails exist.
DUMMY_HASH = hash_password("not-a-real-password")

app = FastAPI(title="Nimbus onboarding assistant")
bearer = HTTPBearer(auto_error=False)


class LoginRequest(BaseModel):
    email: str
    password: str


class AskRequest(BaseModel):
    # Reject unknown fields, so a client can't even try to send an email or
    # department. Identity only ever comes from the token.
    model_config = ConfigDict(extra="forbid")

    question: str = Field(min_length=1, max_length=1000)


class GoalStatusRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal[progress.GOAL_STATUSES]


def public(user):
    return {k: user[k] for k in ("email", "name", "department", "title")}


def unauthorized(detail):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def make_token(email):
    now = datetime.now(timezone.utc)
    claims = {"sub": email, "iat": now, "exp": now + timedelta(hours=TOKEN_HOURS)}
    return jwt.encode(claims, JWT_SECRET, algorithm=JWT_ALGORITHM)


def current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)):
    """The logged-in user, from the token only. Every protected endpoint uses this."""
    if credentials is None:
        raise unauthorized("Not logged in")

    try:
        claims = jwt.decode(credentials.credentials, JWT_SECRET,
                            algorithms=[JWT_ALGORITHM], options={"require": ["sub", "exp"]})
    except jwt.ExpiredSignatureError:
        raise unauthorized("Session expired, please log in again")
    except jwt.InvalidTokenError:
        raise unauthorized("Invalid token")

    # Department is looked up fresh, so a removed user or a department change
    # takes effect immediately instead of when their token expires.
    with psycopg.connect(DATABASE_URL) as conn:
        user = get_user(conn, claims["sub"])
    if user is None:
        raise unauthorized("Invalid token")
    return user


@app.post("/login")
def login(body: LoginRequest):
    email = body.email.strip().lower()
    with psycopg.connect(DATABASE_URL) as conn:
        user = get_user(conn, email)

    stored = user["password_hash"] if user else DUMMY_HASH
    if not check_password(body.password, stored) or user is None:
        raise unauthorized("Incorrect email or password")

    return {
        "access_token": make_token(user["email"]),
        "token_type": "bearer",
        "expires_in": TOKEN_HOURS * 3600,
        "user": public(user),
    }


@app.get("/me")
def me(user=Depends(current_user)):
    return public(user)


@app.get("/demo-users")
def demo_users():
    """Names and roles for the login page. No passwords or hashes."""
    with psycopg.connect(DATABASE_URL) as conn:
        rows = conn.execute(
            "SELECT email, name, department, title FROM users ORDER BY department, name"
        ).fetchall()
    return [dict(zip(("email", "name", "department", "title"), row)) for row in rows]


@app.post("/ask")
def ask(body: AskRequest, user=Depends(current_user)):
    start = time.perf_counter()
    # Always the hybrid retriever (dense + keyword search, fused).
    result = answer(body.question.strip(), user["email"], user["department"])
    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "seconds": round(time.perf_counter() - start, 2),
    }


def not_found():
    # Same answer for "doesn't exist" and "belongs to someone else", so ids
    # can't be probed to learn about other users' items.
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")


@app.get("/dashboard")
def dashboard(user=Depends(current_user)):
    email = user["email"]
    today = datetime.now().date()
    start_date = user["start_date"] or today
    days = (today - start_date).days

    with psycopg.connect(DATABASE_URL) as conn:
        goals = progress.get_goals(conn, email)
        checklist = progress.get_checklist(conn, email)
        feedback = progress.get_feedback(conn, email)
        manager = get_user(conn, user["manager_email"]) if user["manager_email"] else None
        summary = weekly_summary(conn, email, goals, checklist, start_date)

    phase = progress.current_phase(days)
    phase_goals = [g for g in goals if g["phase"] == phase]

    return {
        "profile": {
            **public(user),
            "manager": {"email": manager["email"], "name": manager["name"]} if manager else None,
            "start_date": start_date,
            "days_at_nimbus": days,
        },
        "stats": {
            "days_at_nimbus": days,
            "current_phase": phase,
            "goals_done": sum(g["status"] == "done" for g in phase_goals),
            "goals_total": len(phase_goals),
            "checklist_done": sum(c["done"] for c in checklist),
            "checklist_total": len(checklist),
            "new_feedback": sum(f["is_new"] for f in feedback),
        },
        "goals": goals,
        "checklist": checklist,
        "feedback": feedback,
        "up_next": progress.up_next(goals, checklist),
        "summary": summary,
    }


@app.post("/checklist/{item_id}/toggle")
def toggle_checklist(item_id: int, user=Depends(current_user)):
    with psycopg.connect(DATABASE_URL) as conn:
        item = progress.toggle_checklist_item(conn, user["email"], item_id)
    if item is None:
        raise not_found()
    return item


@app.post("/goals/{goal_id}/status")
def set_goal_status(goal_id: int, body: GoalStatusRequest, user=Depends(current_user)):
    with psycopg.connect(DATABASE_URL) as conn:
        goal = progress.set_goal_status(conn, user["email"], goal_id, body.status)
    if goal is None:
        raise not_found()
    return goal
