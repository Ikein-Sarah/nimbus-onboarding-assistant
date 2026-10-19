import json
import os
import re
from dotenv import load_dotenv
from openai import OpenAI

from pathlib import Path
from app.documents import parse_file
from app.retrievers import tools as fs

load_dotenv()

MODEL = "gpt-4o"
MAX_STEPS = 12

client = OpenAI()

SYSTEM_PROMPT = """
You are searching a company's document folders to find the documents needed
to answer an employee's question.

How to work:
- Start with list_folder on "data" to see what you can reach.
- Use grep to find which documents mention terms from the question.
- grep only matches exact words. Documents often use different words from
  the question, so if a search finds nothing, try synonyms and related
  terms before giving up. For example, "wifi" might appear as "network",
  "boss" as "manager", and "login" as "access". Also try single words
  instead of phrases, and other spellings, for example "color" and "colour".
- If searching still finds nothing, browse the folder that fits the topic
  (finance topics in data/finance, people topics in data/people, and so on)
  and read files whose names look relevant.
- Use read_file to open the documents that look relevant.
- Before you finish, open every document you are going to name with read_file.
  A grep match alone is not enough.

Some folders and files will refuse you. That is normal: it means this
employee is not permitted to see them. Do not try to work around a refusal,
and do not guess at what refused content might say.

When you have finished searching, reply with the file paths you found, or
NONE if nothing you could reach answers the question. Do not answer the
question yourself.
"""

TOOL_SCHEMAS = [
    {
        "type": "function",
        "name": "list_folder",
        "description": "List the files and folders inside a folder.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Folder path, for example data or data/engineering",
                }
            },
            "required": ["path"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "grep",
        "description": (
            "Search every document this employee can access for a word or "
            "phrase. Returns matching lines with their file and line number."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "A single word or short phrase to search for",
                }
            },
            "required": ["pattern"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "read_file",
        "description": "Read a whole document.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "File path, for example data/general/leave-policy.md",
                }
            },
            "required": ["path"],
            "additionalProperties": False,
        },
    },
]

REFUSALS = ("Not allowed", "No such file", "Not a folder")


def run_tool(name, arguments, email, department):
    if name == "list_folder":
        return fs.list_folder(arguments["path"], email, department)
    if name == "grep":
        return fs.grep(arguments["pattern"], email, department)
    if name == "read_file":
        return fs.read_file(arguments["path"], email, department)
    return f"Unknown tool: {name}"


def retrieve_with_stats(question, email, department):
    conversation = [{"role": "user", "content": question}]
    opened = []
    stats = {"tool_calls": 0, "steps": 0, "refused": 0, "bad_calls": 0}

    for _ in range(MAX_STEPS):
        response = client.responses.create(
            model=MODEL,
            instructions=SYSTEM_PROMPT,
            input=conversation,
            tools=TOOL_SCHEMAS,
        )
        stats["steps"] += 1

        calls = [item for item in response.output if item.type == "function_call"]
        if not calls:
            break

        conversation += response.output

        for call in calls:
            stats["tool_calls"] += 1
            try:
                arguments = json.loads(call.arguments)
                result = run_tool(call.name, arguments, email, department)
            except (json.JSONDecodeError, KeyError) as error:
                stats["bad_calls"] += 1
                arguments = {}
                result = f"Tool call failed: {error}. Check the arguments and try again."

            failed = result.startswith("Tool call failed")
            if result.startswith(REFUSALS):
                stats["refused"] += 1
            elif call.name == "read_file" and not failed and arguments["path"] not in opened:
                opened.append(arguments["path"])

            conversation.append({
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": result,
            })

    # The agent sometimes names a file it only saw in grep results. Open those
    # through fs.read_file so the same permission check applies.
    for path in re.findall(r"data/[\w./@-]+\.md", response.output_text):
        if path not in opened:
            result = fs.read_file(path, email, department)
            if not result.startswith(REFUSALS):
                opened.append(path)

    chunks = []
    for path in opened:
        doc = parse_file(Path(path))
        chunks.append({
            "text": doc["text"],
            "path": doc["path"],
            "department": doc["department"],
            "owner": doc["owner"],
        })

    return chunks, stats


def retrieve(question, email, department):
    chunks, _ = retrieve_with_stats(question, email, department)
    return chunks


if __name__ == "__main__":
    question = "The glossary mentions people/salary-bands.md. What is in that file?"

    for email, dept in [("tunde@nimbuslabs.io", "people"),
                        ("sarah@nimbuslabs.io", "engineering")]:
        print(f"\n=== {email} ({dept}) ===")
        chunks, stats = retrieve_with_stats(question, email, dept)
        print(stats)
        for c in chunks:
            print(" ", c["path"])