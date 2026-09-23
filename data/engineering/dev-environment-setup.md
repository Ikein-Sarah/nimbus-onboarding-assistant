---
title: Development Environment Setup
department: engineering
owner: all
effective: 2026-03-01
summary: How to get the Nimbus codebase running locally, including Docker and database setup.
---

# Development Environment Setup

Last updated by: sarah@nimbuslabs.io (first doc she touched after
onboarding — see `onboarding-checklist.md` week 1)

## Prerequisites

Docker Desktop, Python 3.12, Node 20, and the gcloud CLI. If any of these
aren't installed, `make check-prereqs` will tell you what's missing
rather than failing partway through setup with a confusing error.

## Getting the code

Clone the monorepo from github.com/nimbuslabs/platform. Access is
granted to engineering staff on day 1. If you cannot clone, your GitHub
account is not yet in the engineering team group — this is the single
most common day-1 blocker, flag it in the engineering channel rather
than troubleshooting your SSH keys for an hour.

## Running locally

Copy .env.example to .env, then run `docker compose up`. This starts the
API, the worker, Postgres, and Redis. The API is served on port 8000.

### Services this starts

| Service | Port | Notes |
|---|---|---|
| API | 8000 | Main entry point |
| Worker | n/a | Background jobs, no exposed port |
| Postgres | 5432 | See "Common problems" below |
| Redis | 6379 | Used for queues and caching |

## Database

Run `make db-migrate` to apply migrations and `make db-seed` to load
sample data. Never point your local environment at the production
database — there is no technical safeguard preventing this, it's a hard
social rule, so double-check your connection string if you've ever
touched it manually.

## Common problems

- **Port 5432 already in use** usually means a local Postgres is
  running. Stop it or change the port mapping in
  docker-compose.override.yml.
- **Can't clone the repo** — see "Getting the code" above, almost always
  a GitHub team membership issue, not a git problem.
- **API returns 500 on every request** — usually means migrations
  haven't been run yet. Run `make db-migrate` before `make db-seed`, not
  after.

## Getting help

Ask in the engineering Slack channel. Your onboarding buddy is your
first point of contact for the first two weeks, per
`onboarding-checklist.md`. After that, the channel is still the right
default — most "how do I..." questions have already been asked there
once.

## TODO

- Document the M-series Mac Docker performance workaround — comes up
  often enough now that it should be written down instead of re-explained
  in Slack each time.
