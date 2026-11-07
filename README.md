# Nimbus

Nimbus is an AI workplace assistant for employees. It answers questions using only the company documents each person is allowed to see, tracks goals and manager feedback, and guides new hires through onboarding.

![Home in dark mode](docs/screenshots/home-dark.jpg)

| Ask Nimbus chat | My goals | Sign in |
|---|---|---|
| ![Home with the chat open](docs/screenshots/home-chat-open.jpg) | ![My goals](docs/screenshots/my-goals.jpg) | ![Sign-in page](docs/screenshots/sign-in.jpg) |

## Features

- **Ask Nimbus side chat.** Ask how things work at the company. Answers come only from documents you can see and name the files they used. If the answer isn't there, it says so.
- **AI weekly summary.** A short summary of your week, written to you, with what's done, what's due soon and what to do next.
- **Goals with manager feedback.** Your 30, 60 and 90 day goals, and notes from your manager.
- **Onboarding checklist and days at Nimbus** for new hires.
- **Light and dark mode**, remembered in your browser.

## How it works

1. You sign in. The server gives you a token that says who you are.
2. You ask a question. The server reads your identity and department from the token.
3. Hybrid search looks through the documents you are allowed to see, by meaning (pgvector) and by exact words (Postgres full-text search), and merges the two result lists.
4. GPT-4o answers from those documents only, and the chat shows the source files the answer cites.

Each document has a header saying which department and which person can see it:

| Folder | Who can see it |
|---|---|
| `data/general/` | Everyone |
| `data/engineering/`, `growth/`, `people/`, `finance/` | Only that department |
| `data/personal/<email>/` | Only that one person |

## Security

- Your identity comes from the login token, never from the request. The API rejects requests that try to send an email or department.
- Access control happens in retrieval, not the prompt. Documents you can't see are filtered out in SQL, so the model never receives them.
- You can only see and change your own goals and checklist items. Other people's items return 404, the same as items that don't exist.
- Passwords are hashed with bcrypt.
- Tokens expire after 4 hours.

## Evaluation

I compared two ways to find documents on the same 60 documents and 32 questions:

- **Hybrid search:** vector search plus keyword search, merged with Reciprocal Rank Fusion.
- **Agentic file search:** a GPT-4o agent that browses folders with `list_folder`, `grep` and `read_file`, with the same permission check on every tool call.

The questions cover simple lookups, multi-step questions, outdated policies, questions with no answer, and access traps (for example, an engineer asking for salary bands). A GPT-4o judge scores each answer out of 10, and 7 or more is a pass.

| | Hybrid v1 | Agent v1 | Hybrid v2 | Agent v2 |
|---|---|---|---|---|
| Passed | 26/32 | 23/32 | 25/32 | 25/32 |
| Right document found | 22/23 | 18/23 | 22/23 | 22/23 |
| Average time | 2.4s | 8.7s | 2.4s | 9.7s |
| Leaks of restricted documents | 0 | 0 | 0 | 0 |

"Right document found" counts the 23 questions that have an expected source file. Results are in `eval/results-v1.json` and `eval/results-v2.json`.

**The bug:** in v1 the agent found answers with `grep` but didn't open the files, so it answered from files it had never read. **The fix:** the agent now has to open every file it names, tries other words when a search finds nothing, and any file it names but didn't open is read through the same permission check. That brought it level with hybrid search on accuracy, but it is still about 4 times slower, so the app uses hybrid search.

![Hybrid search vs agentic file search](docs/architecture.png)

## Tech stack

- Python, FastAPI
- Postgres + pgvector
- OpenAI: `gpt-4o` and `text-embedding-3-small`
- React + Vite
- Docker

## Run it locally

You need Docker, Python 3, Node 20.19 or newer, and an OpenAI API key.

```bash
# 1. Get the code
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

```bash
# 3. Start the database
docker compose up -d

# 4. Install Python packages
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 5. Add the demo users, their goals and checklists, and embed the documents
python -m app.users
python -m app.progress
python -m app.embed

# 6. Start the backend
uvicorn app.api:app --reload --port 8001
```

```bash
# 7. In a second terminal, start the frontend
cd frontend
npm install
npm run dev
```

8. Open http://localhost:5173 and sign in as `sarah@nimbuslabs.io` with the `DEMO_PASSWORD` from your `.env`.

Other demo users are in `data/users.seed.json`. Try asking about salary bands as Sarah (engineering) and then as `tunde@nimbuslabs.io` (people) to see access control in action.

## What's next

- Deploy it online
- An HR invite flow for new employees
- A report of questions the assistant couldn't answer
