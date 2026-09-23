---
title: Deployment Process
department: engineering
owner: all
effective: 2026-04-10
summary: How code reaches staging and production, release windows and rollback steps.
---

> **Archived.** Superseded by `deployment-process-v2.md`, effective
> 2026-08-15, which adds canary rollouts and mandatory feature flags for
> auth/billing/deletion changes. The environments, release window, and
> migration rules below are still accurate; the "Releasing to production"
> section is not — there's a canary step now.

# Deployment Process

## Environments
We run three environments: local, staging, and production. Staging mirrors
production and is redeployed on every merge to main.

## Releasing to production
Production deploys happen on demand through the release pipeline. A deploy
requires a green CI run, one approving review, and a filled release note.

## Release windows
No production deploys after 16:00 on Fridays, and none during a customer
freeze window. Freeze windows are announced in the engineering channel.

## Rollback
Every deploy is tagged. To roll back, re-run the pipeline against the previous
tag. Rollbacks do not need approval. Announce the rollback in the incident
channel.

## Database migrations
Migrations deploy separately from application code and must be backward
compatible for at least one release.
