import json
from pathlib import Path

questions = {q["id"]: q for q in json.loads(Path("eval/questions.json").read_text(encoding="utf-8"))}
results = json.loads(Path("eval/results.json").read_text(encoding="utf-8"))

by_id = {}
for r in results:
    by_id.setdefault(r["id"], {})[r["route"]] = r


def mark(r):
    if r is None:
        return "not run"
    status = "PASS" if r["passed"] else "FAIL"
    leak = " | LEAK" if r["leaked"] else ""
    return f"{status} ({r['score']}/10){leak}"


def reason(r):
    # Results from before the judge gave reasons have no judge_reason.
    return (r or {}).get("judge_reason") or "no reason recorded"


lines = ["# Eval review", "",
         "Each question shows the answer key, then what each route said.",
         "Judge them yourself: the score is the model judge's opinion, not the truth.", ""]

failed = [i for i, rs in by_id.items() if any(not r["passed"] for r in rs.values())]
lines.append(f"**Questions with at least one FAIL:** {', '.join(f'Q{i}' for i in sorted(failed)) or 'none'}")
lines.append("")

for qid in sorted(by_id):
    q = questions[qid]
    rs = by_id[qid]
    v, a = rs.get("vector"), rs.get("file agent")
    lines += [
        "---", "",
        f"## Q{qid} · {q['type']} · asked as {q['email']}",
        "",
        f"**Question:** {q['question']}",
        "",
        f"**Answer key:** {q['expected']}",
        "",
        f"**Expected sources:** {', '.join(q['expected_sources']) or 'none'}",
        "",
        f"**Vector** — {mark(v)}",
        "",
        f"> {v['answer'] if v else ''}",
        "",
        f"*Judge:* {reason(v)}",
        "",
        f"**File agent** — {mark(a)}" + (f" · {a['tool_calls']} tool calls" if a and a.get('tool_calls') else ""),
        "",
        f"> {a['answer'] if a else ''}",
        "",
        f"*Judge:* {reason(a)}",
        "",
        "**Your verdict:** ",
        "",
    ]

Path("eval/review.md").write_text("\n".join(lines), encoding="utf-8")
print(f"wrote eval/review.md with {len(by_id)} questions, {len(failed)} with a fail")
