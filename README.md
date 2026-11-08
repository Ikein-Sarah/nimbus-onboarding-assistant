# Nimbus

Nimbus is an AI workplace assistant for employees. It answers questions using only the company documents each person is allowed to see, tracks goals and manager feedback, and guides new hires through onboarding.

**Live demo:** https://nimbus-web-usyl.onrender.com

**Demo login:** `sarah@nimbuslabs.io` / `012345678`

First load may take a minute while the free server wakes up.

**Demo video:** coming soon

<!-- To add the video, replace VIDEO_ID (the part after watch?v= in the YouTube link) and uncomment:
[![Nimbus demo video](https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg)](https://www.youtube.com/watch?v=VIDEO_ID)
-->

![Home in dark mode](docs/screenshots/home-dark.jpg)

| Ask Nimbus chat | My goals | Sign in |
|---|---|---|
| ![Home with the chat open](docs/screenshots/home-chat-open.jpg) | ![My goals](docs/screenshots/my-goals.jpg) | ![Sign-in page](docs/screenshots/sign-in.jpg) |

## Features

- **Ask Nimbus chat.** Answers come only from documents you can see, and name the files they used. If the answer isn't there, it says so.
- **AI weekly summary.** What's done, what's due soon and what to do next.
- **Goals and manager feedback.** Your 30, 60 and 90 day goals, and notes from your manager.
- **Onboarding checklist** for new hires.
- **Light and dark mode.**

## Side experiment

While building Nimbus I also ran a side experiment comparing two ways of finding answers in company documents: hybrid search (vector + keyword search) and agentic file search (an AI agent that lists folders, searches and reads files). The live app uses hybrid search. The comparison is in the [Evaluation](#evaluation) section.

## Architecture

```mermaid
%%{init: {"theme": "base", "themeVariables": {"fontSize": "16px", "lineColor": "#D29A63"}}}%%
flowchart LR
    A["Browser<br/>React app on Render"] --> B["FastAPI backend<br/>on Render"]
    B --> C[("Postgres + pgvector<br/>on Neon")]
    B --> D["OpenAI<br/>embeddings, answers,<br/>weekly summary"]
    classDef app fill:#3B2216,stroke:#3B2216,color:#F6F0E9
    classDef ext fill:#F6F0E9,stroke:#D29A63,stroke-width:2px,color:#3B2216
    class A,B app
    class C,D ext
```

How a question is answered:

1. You sign in and get a token that says who you are.
2. Your question goes to the backend with that token.
3. Hybrid search (vector + keyword, merged with Reciprocal Rank Fusion) looks only through documents you are allowed to see.
4. GPT-4o answers from those documents and lists its sources.

Each document says who can see it: everyone (`data/general/`), one department (`data/engineering/`, `growth/`, `people/`, `finance/`), or one person (`data/personal/<email>/`).

## Security

- Your identity comes from the login token, never from the request.
- Access control happens in retrieval. Documents you can't see are filtered out in SQL, so the model never receives them.
- You can only see and change your own goals and checklist. Other people's items return 404.
- Passwords are hashed with bcrypt.
- Tokens expire after 4 hours.
- Rate limits protect the OpenAI budget (see Demo limits).

## Evaluation

**Goal.** Find out which approach answers more questions correctly, finds the right document more often, is faster, and never shows anyone a document they're not allowed to see.

**How each approach works.**

- **Hybrid search:** documents are split into chunks and embedded into Postgres with pgvector. Each question runs a vector search and a Postgres full-text search, and the two lists are merged with Reciprocal Rank Fusion. The permission filter runs in the SQL query, before ranking.
- **Agentic file search:** a gpt-4o agent with three tools, `list_folder`, `grep` and `read_file`, and up to 12 steps. The permission check runs inside every tool.
- Both use the same answer step (gpt-4o) and the same permission rules.

![Hybrid search vs agentic file search](docs/search-comparison.svg)

**How it was tested.** The same 60 documents and the same 32 questions, including 6 access traps (for example, an engineer asking for salary bands) and 3 questions with no answer in the documents. gpt-4o judged each answer.

| | Hybrid search | Agentic file search |
|---|---|---|
| Questions passed | 25/32 | 25/32 |
| Right document found | 22/23 | 22/23 |
| Average time | 2.4s | 9.7s |
| Restricted documents leaked | 0 | 0 |

I wrote about the full comparison here: [Hybrid search vs agentic file search: which approach works better?](https://medium.com/@ikein_sarah/hybrid-search-vs-agentic-file-search-which-approach-works-better-82a64798b466)

## Tech stack

Python, FastAPI, Postgres + pgvector, OpenAI (`gpt-4o`, `text-embedding-3-small`), React + Vite, Docker, Render, Neon

## Run it locally

You need Docker, Python 3, Node 20.19 or newer, and an OpenAI API key.

1. Get the code:

```bash
git clone https://github.com/Ikein-Sarah/nimbus-onboarding-assistant.git
cd nimbus-onboarding-assistant
```

2. Create a `.env` file in the project folder:

```
OPENAI_API_KEY=your-openai-key
DATABASE_URL=postgresql://nimbus:nimbus@localhost:5434/nimbus
JWT_SECRET=any-random-string-of-at-least-32-characters
DEMO_PASSWORD=a-password-for-the-demo-users
```

3. Start the database, set up the tables and data, and run the backend:

```bash
docker compose up -d
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m scripts.setup_db
uvicorn app.api:app --reload --port 8001
```

4. In a second terminal, run the frontend:

```bash
cd frontend
npm install
npm run dev
```

5. Open http://localhost:5173 and sign in as `sarah@nimbuslabs.io` with your `DEMO_PASSWORD`.

## Deploy it

1. Create a free Neon project and copy its connection string.
2. Set up the database once from your laptop:

```bash
DATABASE_URL='your-neon-connection-string' python -m scripts.setup_db
```

3. On Render, create a Blueprint from this repo. `render.yaml` defines both services:
   - `nimbus-api`: set `DATABASE_URL`, `OPENAI_API_KEY` and `FRONTEND_URL` (the website address).
   - `nimbus-web`: set `VITE_API_URL` (the API address).

## Demo limits

- 10 questions per hour and 30 per day per visitor
- 200 AI calls per day overall
- The weekly summary is regenerated at most once an hour per user

## What's next

- HR invite flow for new employees
- Custom domain
