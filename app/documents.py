from pathlib import Path
import yaml

DATA_DIR = Path("data")
REQUIRED = ("title", "department", "owner")


def parse_file(path):
    raw = path.read_text(encoding="utf-8")

    if not raw.startswith("---"):
        raise ValueError(f"No YAML header: {path}")

    _, header, body = raw.split("---", 2)
    meta = yaml.safe_load(header)

    for field in REQUIRED:
        if field not in meta:
            raise ValueError(f"Missing '{field}' in {path}")

    return {
        "path": str(path),
        "department": meta["department"],
        "owner": meta["owner"],
        "title": meta["title"],
        "text": body.strip(),
    }


def load_documents(data_dir=DATA_DIR):
    files = sorted(data_dir.rglob("*.md"))
    return [parse_file(p) for p in files if p.parent != data_dir]


def visible_documents(docs, email, department):
    visible = []
    for doc in docs:
        dept_ok = doc["department"] in ("general", department)
        owner_ok = doc["owner"] in ("all", email)
        if dept_ok and owner_ok:
            visible.append(doc)
    return visible


if __name__ == "__main__":
    docs = load_documents()
    print(f"{len(docs)} documents\n")

    people = [
        ("sarah@nimbuslabs.io", "engineering"),
        ("amaka@nimbuslabs.io", "growth"),
        ("tunde@nimbuslabs.io", "people"),
    ]

    for email, dept in people:
        mine = visible_documents(docs, email, dept)
        print(f"{email} ({dept}): {len(mine)} documents")

    sarah = visible_documents(docs, "sarah@nimbuslabs.io", "engineering")
    paths = [d["path"] for d in sarah]
    print("\nSarah sees salary bands:", any("salary-bands" in p for p in paths))
    print("Sarah sees John's letter:", any("john@nimbuslabs.io" in p for p in paths))