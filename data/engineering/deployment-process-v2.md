---
title: Deployment Process v2 (Canary Releases)
department: engineering
owner: all
effective: 2026-08-15
summary: Replaces the 2026-04 Deployment Process. Adds canary rollouts and mandatory feature flags for risky changes.
---

# Deployment Process v2 (Canary Releases)

> Supersedes `deployment-process.md` (effective 2026-04-10). That document
> is archived but not deleted — some of it (environments, database
> migrations) is still accurate and referenced below instead of repeated.

Last updated by: daniel@nimbuslabs.io

## Why this changed

The March outage (`incident-postmortem-2026-03-outage.md`) traced back to
a deploy that went straight to 100% of production traffic with no gradual
rollout. The fix from that postmortem's action items was to introduce
canary releases. This doc is that fix, written up as the new standard
process.

## What's still true from v1

Unchanged from `deployment-process.md`, not repeated in full here:

- Three environments: local, staging, production.
- Staging redeploys automatically on every merge to main.
- No production deploys after 16:00 on Fridays, or during a freeze window.
- Database migrations deploy separately and must be backward compatible
  for at least one release.

## What's new: canary rollout

1. A deploy requires a green CI run, one approving review, and a filled
   release note — same as before.
2. The release pipeline now deploys to 5% of production traffic first
   ("the canary") and holds for 15 minutes.
3. Datadog dashboards are checked automatically for error rate and
   latency regressions during the hold. If thresholds are breached, the
   canary is auto-rolled-back and the release pipeline pages the deploy
   author.
4. If the canary holds clean, the deploy author manually promotes to
   100%. This step is **not** automatic — someone has to actually look and
   click promote.

## Feature flags are now mandatory for risky changes

Any change touching authentication, billing, or data deletion (the same
categories that need two review approvals per
`code-review-guidelines.md`) must ship behind a feature flag, even if
you intend to enable it for 100% of users immediately after deploy. This
lets us disable a bad change without a full rollback.

This is a genuinely new requirement — it did not exist under v1, and
older engineering onboarding material may not mention it yet. If you
onboarded before August 2026, this is likely new to you.

## Rollback

Same mechanic as v1: every deploy is tagged, rollback re-runs the pipeline
against the previous tag, no approval needed, announce it in the incident
channel. The canary step means rollbacks should be rarer now, but the
mechanism itself hasn't changed.

## What did NOT change

- Release windows (still no Friday afternoon deploys)
- Database migration rules
- Who can trigger a deploy (any engineer with a green CI run and an
  approval — this was never restricted to leads)

## Rollout of this process itself

This process is mandatory for all services as of 2026-09-01. A few
smaller internal services haven't been migrated to the canary pipeline
yet — check with Daniel before assuming a given service already has it.
