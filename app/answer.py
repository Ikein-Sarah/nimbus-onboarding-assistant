import os
from dotenv import load_dotenv
from openai import OpenAI

from app.retrievers.vector import retrieve

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

3. When the documents do not answer the question, reply with this exact
   sentence and nothing else, with no quotation marks around it:
   I couldn't find information about that in the documents available to you.
   Do not guess, and do not speculate about why the information is missing.

4. Check effective dates. Some policies have been replaced by newer versions.
   When two documents conflict, use the one with the later effective date and
   mention that an earlier version exists.

5. Keep answers short. Two or three sentences for a simple question. Use a
   short list only when the answer genuinely has several parts.

6. Write plainly, the way a helpful colleague would. No preamble, no
   restating the question, no offers to help further.
"""


def build_context(chunks):
    parts = []
    for chunk in chunks:
        parts.append(f"source: {chunk['path']}\n {chunk['text']}")
        pass
    return "\n\n".join(parts)


def answer(question, email, department):
    chunks = retrieve(question, email, department)
    context = build_context(chunks)

    user_message = f"company document: \n\n{context}\n\nQuestion: {question}"
    response = client.responses.create(
        model= MODEL,
        instructions= SYSTEM_PROMPT,
        input= user_message,
    )
    text = response.output_text.strip()                      # <-- new
    refused = NO_ANSWER in text

    return {
        "answer": text,                                      # <-- changed
        "sources": [] if refused else sorted({c["path"] for c in chunks}),   # <-- changed
    }


if __name__ == "__main__":
    question = "What is John Mensah's salary?"

    for email, dept in [("tunde@nimbuslabs.io", "people"),
                        ("sarah@nimbuslabs.io", "engineering")]:
        result = answer(question, email, dept)
        print(f"\n=== {email} ===")
        print(result["answer"])
        print("sources:", result["sources"])