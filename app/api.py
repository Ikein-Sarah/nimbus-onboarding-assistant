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

from app.answer import answer
from app.retrievers import file_agent, vector
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


RETRIEVERS = {"vector": vector.retrieve, "file_agent": file_agent.retrieve}


class LoginRequest(BaseModel):
    email: str
    password: str


class AskRequest(BaseModel):
    # Reject unknown fields, so a client can't even try to send an email or
    # department. Identity only ever comes from the token.
    model_config = ConfigDict(extra="forbid")

    question: str = Field(min_length=1, max_length=1000)
    route: Literal["vector", "file_agent"] = "vector"


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
    result = answer(body.question.strip(), user["email"], user["department"],
                    retriever=RETRIEVERS[body.route])
    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "route": body.route,
        "seconds": round(time.perf_counter() - start, 2),
    }
