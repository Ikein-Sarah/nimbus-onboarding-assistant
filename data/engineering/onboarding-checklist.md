---
title: Engineering Onboarding Checklist
department: engineering
owner: all
effective: 2026-06-01
summary: Role-specific onboarding steps for new engineers, on top of the company-wide first-week checklist.
---

# Engineering Onboarding Checklist

Last updated by: john@nimbuslabs.io

Do this alongside `general/new-hire-first-week.md`, not instead of it.
This page assumes you've already got your laptop and accounts.

## Week 1

- [ ] Get added to the GitHub `engineering` team group — if you can't
      clone the monorepo, this is why, see
      `dev-environment-setup.md`
- [ ] Get the local dev environment running (`docker compose up`),
      confirm the API responds on port 8000
- [ ] Get GCP console viewer access (should be automatic — flag Daniel if
      not)
- [ ] Read `code-review-guidelines.md` before opening your first PR
- [ ] Read `deployment-process-v2.md` — yes, even before you've shipped
      anything, so the canary language isn't new to you later
- [ ] Shadow a PR review (watch, don't do the review yet)

## Week 2

- [ ] Open your first PR — small, ideally a starter task from your
      onboarding buddy
- [ ] Read `oncall-rotation.md` in full, even though you won't join the
      rotation for 90 days. Understanding severity levels early helps you
      read incident channels sensibly.
- [ ] Get read access to Datadog, confirm you can find the dashboards for
      the service your team owns

## By day 90

- [ ] Join the on-call rotation, shadowing for one full week first
      (per `oncall-rotation.md`)
- [ ] Have shipped at least one production change through the full
      deploy pipeline, including the canary stage
- [ ] First formal review happens in the next full cycle after day 90 —
      see `people/performance-review-cycle-2026.md`

## Tools checklist (cross-reference)

This overlaps with `general/tooling-and-access-requests.md` — that page
has the full table of what's automatic vs. requested. The short version
for engineers: GitHub and GCP viewer are automatic, GCP admin and prod DB
access are requested separately once you actually need them, not as part
of onboarding by default.

## Who to ask

Your onboarding buddy is your first point of contact for two weeks (per
`dev-environment-setup.md`). After that, use the engineering Slack
channel for anything not personal, and your manager for anything that is.
