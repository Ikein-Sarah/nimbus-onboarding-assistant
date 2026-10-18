# Nimbus Onboarding Assistant

New hires spend their first weeks asking the same questions. How much leave do I get? How do deployments work here? Who do I escalate to when I'm on call? The answers are somewhere in the company wiki, but finding them is slow, and some documents (salary bands, offer letters, budgets) should never be shown to the wrong person.

Nimbus Onboarding Assistant is a RAG assistant that answers new-hire questions from company documents, **only using the documents that employee is allowed to see**. Every answer cites the files it came from, and when the answer isn't in the documents, it says so instead of guessing.

> **Status:** in progress. Retrieval, access control and answer generation work end to end from the command line. An API, login and a front end are next.

## What it does

- **Permission-aware retrieval.** Each employee only retrieves from company-wide docs, their own department's docs, and their own personal folder. Access is enforced in the retrieval layer itself, not left to the LLM.
- **Two retrieval routes to compare:**
  - **Hybrid search**: pgvector similarity search plus Postgres full-text search, merged with Reciprocal Rank Fusion.
  - **File agent**: an LLM agent that explores the document folders with `list_folder`, `grep` and `read_file` tools, the way a person would search a shared drive. Every tool call goes through the same permission check.
- **Grounded answers.** GPT-4o answers only from the retrieved documents, cites each source file, prefers the newer policy when two documents disagree, and refuses when nothing relevant is found.
- **An evaluation set.** 32 test questions covering lookups, multi-hop questions, superseded policies, unanswerable questions and access "traps" (for example, an engineer asking for a colleague's salary).

## Architecture

```mermaid
flowchart TD
    subgraph Ingestion["Ingestion · app/embed.py"]
        direction LR
        D[Company docs<br/>with access headers] --> L[Parse + chunk] --> E[Embed] --> PG[(Postgres + pgvector)]
    end

    U[Employee question<br/>+ email + department] --> R{Which retriever?}

    subgraph Hybrid["Route 1 · Hybrid search"]
        F1[Permission filter in SQL] --> DS[Vector search]
        F1 --> SP[Keyword search]
        DS --> RRF[Rank fusion<br/>top 5 chunks]
        SP --> RRF
    end

    subgraph Agent["Route 2 · File agent"]
        AG[GPT-4o agent loop] <--> T[list_folder · grep · read_file<br/>permission check on every call]
    end

    R --> F1
    R --> AG
    PG -.-> F1
    RRF --> A[Answer with GPT-4o<br/>cite sources · refuse if missing]
    AG --> A
    A --> OUT[Answer + source files]
```

## Access rules

Every document starts with a YAML header that says who can see it:

```yaml
---
title: Leave policy
department: general        # general | engineering | growth | people | finance
owner: all                 # all | <employee email>
effective: 2026-02-01
summary: ...
---
```

| Folder | Who can see it |
|---|---|
| `data/general/` | Everyone |
| `data/engineering/`, `growth/`, `people/`, `finance/` | Only that department |
| `data/personal/<email>/` | Only that one employee |

The same two checks (department and owner) are applied in both routes. In the hybrid route they're part of the SQL `WHERE` clause, so restricted chunks are never retrieved. In the file agent they're applied inside each tool, so the agent gets a "Not allowed" message instead of the file.

## The test company

The repo includes a fictional company, **Nimbus Labs**, so the system can be tested without real data. It has 60 documents (~28,500 words) across four departments, eight employees' personal folders, and a demo roster in `data/users.seed.json`.

The corpus is deliberately messy, like a real wiki. It has older policies that were replaced but are still there, near-duplicate topics across departments, and questions that need two or three documents to answer. See [`data/README.md`](data/README.md) for the full list of built-in test cases.

## Evaluation

`eval/questions.json` holds 32 questions, each with the asking employee, the expected answer and the expected source files:

| Type | Count | What it checks |
|---|---|---|
| lookup | 11 | Simple single-document answers |
| trap | 6 | Questions about documents the user must not see |
| multihop | 4 | Answers that need several documents |
| unanswerable | 3 | Refusing instead of making something up |
| stress tests | 8 | Exact numbers, vague wording, dates, duplicates, partial and personal info |

## Stack

| Concern | Choice |
|---|---|
| Language | Python |
| Database | Postgres 16 + pgvector (Docker) |
| Embeddings | OpenAI `text-embedding-3-small` (1536 dims) |
| Keyword search | Postgres full-text search (`tsvector`, GIN index) |
| Fusion | Reciprocal Rank Fusion (k = 60) |
| Agent + answers | OpenAI Responses API, `gpt-4o`, function calling |
| Chunking | LangChain `RecursiveCharacterTextSplitter` |

## Project structure

```
nimbus-onboarding-assistant/
├── docker-compose.yml        # Postgres + pgvector on port 5434
├── app/
│   ├── documents.py          # load docs, parse YAML headers, visibility rules
│   ├── chunking.py           # split docs into chunks, keep access metadata
│   ├── embed.py              # embed chunks and load them into Postgres
│   ├── answer.py             # build context, call GPT-4o, return answer + sources
│   └── retrievers/
│       ├── vector.py         # hybrid search: dense + full-text + RRF
│       ├── file_agent.py     # agentic file search loop
│       └── tools.py          # permission-gated list_folder / grep / read_file
├── data/                     # Nimbus Labs test corpus + users.seed.json
└── eval/questions.json       # 32-question evaluation set
```

## Running locally

```bash
# 1. Start Postgres with pgvector
docker compose up -d

# 2. Install dependencies
pip install openai psycopg[binary] python-dotenv pyyaml langchain-text-splitters

# 3. Add a .env file
#    OPENAI_API_KEY=...
#    DATABASE_URL=postgresql://nimbus:nimbus@localhost:5434/nimbus

# 4. Embed the documents (run from the repo root)
python -m app.embed

# 5. Ask a question with both retrievers
python -m app.answer
```

`app/answer.py` runs the same question for two employees (one in People, one in Engineering) through both retrievers, so you can see the access control working: the People partner gets the salary bands, the engineer gets a refusal.

## What's next

- Run the evaluation set against both retrievers and publish the results
- API with login, so each user's email and department come from their account
- A simple chat front end
