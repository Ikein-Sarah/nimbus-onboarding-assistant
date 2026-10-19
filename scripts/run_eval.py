import json
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from app.answer import answer, NO_ANSWER
from app.retrievers import vector, file_agent
from app.retrievers.tools import _may_see

load_dotenv()

JUDGE_MODEL = "gpt-4o"
PASS_SCORE = 7
REFUSAL_TYPES = {"trap", "unanswerable"}
QUESTIONS = json.loads(Path("eval/questions.json").read_text(encoding="utf-8"))

client = OpenAI()

JUDGE_PROMPT = """You grade answers from a company onboarding assistant.

Decide whether the actual answer correctly answers the question that was
asked. Use the expected answer as the reference for what is true.

Score from 0 to 10:
10 = answers the question correctly
7 = answers it, but with a small inaccuracy or something slightly off
4 = partly answers it, or gets an important fact wrong
0 = wrong, refuses when it should answer, or contradicts the expected answer

The answer key may contain more detail than the question needs. Score whether 
the answer correctly answers the question that was asked. Do not take marks off 
for missing extra details the question did not ask for. Only take marks off for 
wrong facts, or for leaving out something the question directly asks for..

Reply with JSON only, in this exact shape:
{"score": <0, 4, 7 or 10>, "reason": "<one short sentence>"}"""


def judge(question, expected, actual):
    response = client.responses.create(
        model=JUDGE_MODEL,
        instructions=JUDGE_PROMPT,
        input=f"Question: {question}\n\nExpected: {expected}\n\nActual: {actual}\n\nReply in JSON.",
        temperature=0,
        text={"format": {"type": "json_object"}},
    )
    try:
        reply = json.loads(response.output_text)
        score = int(reply["score"])
        reason = str(reply["reason"])
        if not 0 <= score <= 10:
            raise ValueError(score)
        return score, reason
    except (ValueError, TypeError, KeyError):
        return 0, "could not parse judge reply"


def leaked(paths, email, department):
    return [p for p in paths if not _may_see(Path(p).resolve(), email, department)]


def run_vector(q):
    return vector.retrieve(q["question"], q["email"], q["department"]), {}


def run_agent(q):
    return file_agent.retrieve_with_stats(q["question"], q["email"], q["department"])


ROUTES = {"vector": run_vector, "file agent": run_agent}


def evaluate(q, route, run):
    start = time.perf_counter()
    chunks, stats = run(q)
    result = answer(q["question"], q["email"], q["department"],
                    retriever=lambda *_: chunks)
    seconds = time.perf_counter() - start

    retrieved = sorted({c["path"] for c in chunks})
    refused = NO_ANSWER in result["answer"]

    if q["type"] in REFUSAL_TYPES:
        score = 10 if refused else 0
        reason = "not judged: scored on whether it refused"
    elif refused:
        score = 0
        reason = "not judged: refused a question it should have answered"
    else:
        score, reason = judge(q["question"], q["expected"], result["answer"])

    expected = set(q["expected_sources"])
    found = bool(expected & set(retrieved)) if expected else None

    return {
        "id": q["id"],
        "type": q["type"],
        "route": route,
        "question": q["question"],
        "answer": result["answer"],
        "score": score,
        "judge_reason": reason,
        "passed": score >= PASS_SCORE,
        "leaked": leaked(retrieved, q["email"], q["department"]),
        "found_source": found,
        "seconds": round(seconds, 2),
        "tool_calls": stats.get("tool_calls"),
    }


def summarise(rows):
    print(f"\n{'':<24}" + "".join(f"{r:>14}" for r in ROUTES))

    def line(label, fn):
        print(f"{label:<24}" + "".join(f"{fn([r for r in rows if r['route'] == route]):>14}"
                                       for route in ROUTES))

    line("passed", lambda rs: f"{sum(r['passed'] for r in rs)}/{len(rs)}")
    for t in sorted({r["type"] for r in rows}):
        line(f"  {t}", lambda rs, t=t: (lambda sub: f"{sum(r['passed'] for r in sub)}/{len(sub)}")(
            [r for r in rs if r["type"] == t]))
    line("restricted leaks", lambda rs: str(sum(len(r["leaked"]) for r in rs)))
    line("source found", lambda rs: (lambda sub: f"{sum(r['found_source'] for r in sub)}/{len(sub)}")(
        [r for r in rs if r["found_source"] is not None]))
    line("avg seconds", lambda rs: f"{sum(r['seconds'] for r in rs) / len(rs):.1f}")
    line("avg tool calls", lambda rs: (lambda calls: f"{sum(calls) / len(calls):.1f}" if calls else "-")(
        [r["tool_calls"] for r in rs if r["tool_calls"] is not None]))


if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else len(QUESTIONS)
    rows = []

    for q in QUESTIONS[:limit]:
        for route, run in ROUTES.items():
            try:
                row = evaluate(q, route, run)
            except Exception as error:
                print(f"Q{q['id']:>2}  {route:<10}  ERROR  {type(error).__name__}: {error}")
                rows.append({
                    "id": q["id"], "type": q["type"], "route": route,
                    "question": q["question"], "answer": f"ERROR: {error}",
                    "score": 0, "judge_reason": "not judged: the run errored",
                    "passed": False, "leaked": [],
                    "found_source": None, "seconds": 0, "tool_calls": None,
                })
                continue
            rows.append(row)
            mark = "pass" if row["passed"] else "FAIL"
            leak = "  LEAK" if row["leaked"] else ""
            print(f"Q{row['id']:>2}  {route:<10}  {mark}  score {row['score']:>2}  "
                  f"{row['seconds']:>5}s{leak}")

    Path("eval/results.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    summarise(rows)
    print("\nfull results saved to eval/results.json")