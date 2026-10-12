from pathlib import Path

DATA_DIR = Path("data").resolve()
MAX_MATCHES = 40


def _inside_data(path):
    """Return the resolved path if it sits inside data/, otherwise None."""
    full = Path(path).resolve()
    if full == DATA_DIR or DATA_DIR in full.parents:
        return full
    return None


def _may_see(full, email, department):
    """The two gates, applied to a path."""
    parts = full.relative_to(DATA_DIR).parts
    if not parts:
        return True

    top = parts[0]

    if top == "personal":
        if len(parts) == 1:
            return True
        return parts[1] == email

    return top in ("general", department)


def list_folder(path, email, department):
    full = _inside_data(path)
    if full is None:
        return f"Not allowed: {path} is outside the document folder"
    if not full.is_dir():
        return f"Not a folder: {path}"
    if not _may_see(full, email, department):
        return f"Not allowed: you do not have access to {path}"

    entries = []
    for child in sorted(full.iterdir()):
        if not _may_see(child, email, department):
            continue
        kind = "dir " if child.is_dir() else "file"
        entries.append(f"{kind}  {child.relative_to(DATA_DIR.parent)}")

    if not entries:
        return f"{path} has nothing you can access"
    return f"Contents of {path}:\n" + "\n".join(entries)


def grep(pattern, email, department):
    results = []
    for file in sorted(DATA_DIR.rglob("*.md")):
        if not _may_see(file, email, department):
            continue
        shown = file.relative_to(DATA_DIR.parent)
        lines = file.read_text(encoding="utf-8").splitlines()
        for number, line in enumerate(lines, start=1):
            if pattern.lower() in line.lower():
                results.append(f"{shown}:{number}: {line.strip()}")

    if not results:
        return f"No matches for '{pattern}'"
    return f"Matches for '{pattern}':\n" + "\n".join(results[:MAX_MATCHES])


def read_file(path, email, department):
    full = _inside_data(path)
    if full is None:
        return f"Not allowed: {path} is outside the document folder"
    if not full.is_file():
        return f"No such file: {path}"
    if not _may_see(full, email, department):
        return f"Not allowed: you do not have access to {path}"
    return full.read_text(encoding="utf-8")


if __name__ == "__main__":
    sarah = ("sarah@nimbuslabs.io", "engineering")

    print("--- what Sarah sees at the top ---")
    print(list_folder("data", *sarah))

    print("\n--- inside the personal folder ---")
    print(list_folder("data/personal", *sarah))

    print("\n--- Sarah tries the people folder ---")
    print(list_folder("data/people", *sarah))

    print("\n--- Sarah greps for salary ---")
    print(grep("salary", *sarah))

    print("\n--- Sarah tries John's offer letter ---")
    print(read_file("data/personal/john@nimbuslabs.io/offer-letter.md", *sarah))

    print("\n--- Sarah reads her own ---")
    print(read_file("data/personal/sarah@nimbuslabs.io/offer-letter.md", *sarah)[:200])