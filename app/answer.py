import os
from dotenv import load_dotenv
from openai import OpenAI

from app.retrievers import vector, file_agent

load_dotenv()

MODEL = "gpt-4o"
NO_ANSWER = "I couldn't find information about that"

client = OpenAI()

SYSTEM_PROMPT = """
You are the onboarding assistant for Nimbus Labs. You answer questions from
new employees using only the company documents provided to you.

Rules:

1. Answer only from the provided documents. Do not use outside knowledge, and
   do not fill gaps with what sounds reasonable. If the documents do not
   contain the answer, say so.

2. Cite your sources. After each claim, name the file it came from, like
   (data/general/leave-policy.md). If several documents support an answer,
   cite each of them.

3. Employees often word questions differently from the documents. If the
   documents contain information that addresses the question, answer from
   it, even when the wording differs or the answer is indirect. For example,
   a question about "the office wifi" can be answered from a section on
   network access, and a question asking for a figure can be answered by a
   document saying that figure is confidential or not published.

4. If the documents say something is not offered, not shared or not
   available, tell the user that. That is an answer, not missing
   information. Use the refusal sentence in rule 5 only when the documents
   say nothing about the topic.

5. Only when nothing in the documents addresses the question, reply with
   this exact sentence and nothing else, with no quotation marks around it:
   I couldn't find information about that in the documents available to you.
   Do not guess, and do not speculate about why the information is missing.

6. Check effective dates. Some policies have been replaced by newer versions.
   When two documents conflict, use the one with the later effective date and
   mention that an earlier version exists.

7. Keep answers short. Two or three sentences for a simple question. Use a
   short list only when the answer genuinely has several parts.

8. Write plainly, the way a helpful colleague would. No preamble, no
   restating the question, no offers to help further.
"""


def build_context(chunks):
    parts = []
    for chunk in chunks:
        parts.append(f"[source: {chunk['path']}]\n{chunk['text']}")
    return "\n\n".join(parts)


def answer(question, email, department, retriever=vector.retrieve):
    chunks = retriever(question, email, department)
    context = build_context(chunks)

    user_message = f"Company documents:\n\n{context}\n\nQuestion: {question}"

    response = client.responses.create(
        model=MODEL,
        instructions=SYSTEM_PROMPT,
        input=user_message,
    )

    text = response.output_text.strip()
    refused = NO_ANSWER in text

    return {
        "answer": text,
        "sources": [] if refused else sorted({c["path"] for c in chunks}),
    }


if __name__ == "__main__":
    question = "What is the pay band for a senior engineer?"

    routes = [
        ("vector", vector.retrieve),
        ("file agent", file_agent.retrieve),
    ]

    people = [
        ("tunde@nimbuslabs.io", "people"),
        ("sarah@nimbuslabs.io", "engineering"),
    ]

    for email, dept in people:
        print(f"\n########  {email} ({dept})  ########")
        for name, retriever in routes:
            result = answer(question, email, dept, retriever)
            print(f"\n--- {name} ---")
            print(result["answer"])
            print("sources:", result["sources"])