---
title: Incident Postmortem - 2026-07-09 Canary Rollback
department: engineering
owner: all
effective: 2026-07-11
summary: Sev2. First real-world test of the canary pipeline caught a bug before full rollout, worked as intended.
---

# Incident Postmortem: 2026-07-09 Canary Rollback

Written by: sarah@nimbuslabs.io (first postmortem she led — noted here
only because it came up in her review cycle, not because it matters to
the timeline).

## Summary

Sev2, not Sev1 — this is included as a companion to
`incident-postmortem-2026-03-outage.md` because it's a good example of the
canary process (`deployment-process-v2.md`) working as designed. A bad
deploy was caught at the 5% canary stage and auto-rolled-back before it
reached the rest of production traffic. No customer-facing downtime for
the 95% majority; the 5% canary slice saw elevated error rates for about
11 minutes.

## Impact

- **Customer facing:** roughly 5% of production traffic (the canary
  slice) experienced elevated error rates on the affected worker queue for
  about 11 minutes. The remaining 95% of traffic was entirely unaffected
  — this is the whole point of the canary mechanism described in
  `engineering/architecture-overview.md` section 3.
- **Which customers:** canary traffic routing isn't customer-specific —
  it's a random percentage of requests, so the affected 5% wasn't any
  particular customer segment, just whoever happened to hit the canary
  instance during the window.
- **Data impact:** none. The crash loop caused failed message processing
  (retried automatically once the rollback completed), not data
  corruption.
- **Support load:** 1 ticket, closed without needing an incident-specific
  response — below the threshold where this would normally warrant
  proactive customer communication.

## Timeline

- 13:55 — PR merges after one approval and green CI, per
  `code-review-guidelines.md` — this change didn't touch auth, billing,
  or deletion, so it didn't require the two-approval rule or, at the
  time, a feature flag.
- 14:02 — Deploy of a worker queue change goes to the 5% canary, per
  `deployment-process-v2.md`.
- 14:05 — Canary holds at 5%, initial metrics look normal for the first
  few minutes.
- 14:09 — Error rate on the canary slice crosses the auto-rollback
  threshold in Datadog.
- 14:09 — Pipeline auto-rolls-back the canary and pages the deploy
  author (sarah@nimbuslabs.io) — this happened automatically, no human
  decision was needed to trigger it.
- 14:11 — Sarah acknowledges the page, begins investigating in parallel
  with confirming the rollback landed.
- 14:13 — Sarah confirms the rollback took effect, canary slice healthy
  again. No promotion to 100% ever happened, per the process — the
  canary never got the chance to affect the rest of production.
- 14:20 — Root cause found: a queue consumer config change had an
  off-by-one in a retry count that caused a crash loop under specific
  message shapes.
- 14:28 — Sarah posts a short update in the engineering channel
  confirming impact was limited to the canary slice and no further
  action was urgently needed.
- 14:35 — Fix identified, not yet deployed (postmortem written before the
  fix shipped, per the 3-working-day rule in `oncall-rotation.md`).
- 2026-07-10 — Fix deployed the next day, itself going through the
  canary stage uneventfully.

## Root cause

A retry-count config value was read as a string in one code path and an
integer in another, after a partial refactor. Under the canary's small
traffic slice this triggered quickly because of how message batching
happened to distribute that day. Under the old 100%-at-once process this
same bug would likely have affected significantly more traffic before
anyone noticed — this is called out explicitly as a case where the
canary process did its job.

### The specific bug

The refactor split a single config-loading function into two: one for
the queue consumer's initial setup (which parsed the retry count as an
integer, correctly) and one for a newer hot-reload path added to let the
retry count change without a full redeploy (which read the same value
from a different config source, as a string, and never cast it). Under
most message shapes the string vs. integer distinction never surfaced,
because the retry-count comparison happened to work the same way either
type. Under a specific message shape — one that hit the retry-count
comparison in a loop rather than once — the type mismatch caused an
infinite retry rather than a bounded one, which is what produced the
crash loop.

### Why it wasn't caught earlier

The hot-reload path was new enough (shipped about 3 weeks prior) that it
hadn't yet seen the specific message shape that triggered the bug in
staging or in earlier production traffic. This is a case where more
time in production, not more code review, would likely have surfaced it
eventually — which is itself an argument for the canary approach: it
compresses "more time in production" into a much smaller blast radius.

## What went well

- The whole point of the March action items — catch this kind of thing
  small. It worked, on the first real test.
- Auto-rollback fired without anyone needing to make a judgment call
  under pressure.
- Sarah, first time leading a postmortem, followed the format correctly
  on the first attempt using the March postmortem as a template, which
  is exactly what that template is for.
- The whole incident, from deploy to confirmed-resolved, took under 15
  minutes — a sharp contrast with the 42-minute March outage, even
  accounting for the difference in severity.

## What went wrong

- The type inconsistency (string vs int) should have been caught by
  tests or a stricter config schema, not by production traffic, even a
  small slice of it.

## Action items

| Action | Owner | Status |
|---|---|---|
| Add schema validation for worker queue config | sarah@nimbuslabs.io | Open |
| Document canary-catch incidents as a category, distinct from full outages | daniel@nimbuslabs.io | Done — this doc |
| Audit other config values in the worker for similar type-ambiguity risk | sarah@nimbuslabs.io | Open |
| Add config schema validation to the PR template checklist | john@nimbuslabs.io | Open |

## Detection detail

The specific Datadog alert that fired was an error-rate-per-instance
check scoped to the canary tag, distinct from the fleet-wide error-rate
alert that caught the March incident. This canary-scoped alert was added
as part of the `deployment-process-v2.md` rollout specifically so a
canary-only problem wouldn't have to wait for fleet-wide thresholds to
trip — those are tuned to tolerate normal noise across 100% of traffic
and would have taken much longer to notice a problem confined to 5% of
it. This is a small but important detail: the canary mechanism only
works as fast as it did here because the alerting was built to match it,
not just because a canary stage existed.

## Why this postmortem exists at all

Sev3 and smaller Sev2 incidents don't always get a written postmortem in
practice — the 3-working-day rule in `oncall-rotation.md` technically
applies to all severities, but low-impact issues sometimes get a brief
Slack note instead. This one got the full treatment deliberately, as the
first real production test of the canary process introduced after the
March outage. Its value is less about this specific bug and more about
demonstrating the new process worked exactly as designed.

## How the on-call engineer's day actually looked

Worth including for anyone trying to understand what a canary-catch
incident feels like to live through, since it's meaningfully different
from a full outage: Sarah was mid-way through an unrelated task when the
page came in. Because the rollback was already automatic by the time she
opened her laptop, there was no "stop the bleeding" urgency the way
there was in March — her first 10 minutes were spent confirming the
automatic rollback had actually worked correctly, not manually
triggering any mitigation herself. This is a meaningfully lower-stress
shape of incident, and part of why `oncall-rotation.md`'s Sev2 response
window (60 minutes, not 15) is appropriate here — there's more slack in
the response because the blast radius was already contained
automatically before a human needed to act.

## What this incident does and doesn't prove

It's tempting to read this postmortem as "the canary process solved the
problem, done." That's mostly true but worth qualifying: the canary
caught this specific class of bug — one that manifests quickly and
clearly as an elevated error rate. It would not necessarily catch a bug
that degrades something more subtle (a slow data-correctness issue that
doesn't trip an error-rate threshold, for instance) within the 15-minute
canary hold window. The canary process narrows blast radius for the bugs
it's good at catching; it isn't a general substitute for testing or
review, and shouldn't be treated as one when deciding how much test
coverage a change actually needs before merging.

## Comparison with the March outage

| | March 2026-03-18 | July 2026-07-09 |
|---|---|---|
| Severity | Sev1 | Sev2 |
| Rollout stage when caught | None — 100% immediately | 5% canary |
| Customer impact | Full checkout down, all customers | 5% of traffic, one queue |
| Duration | 42 minutes | 11 minutes |
| Detection | Alert-driven, human-triggered rollback | Alert-driven, automatic rollback |
| Root cause category | Schema mismatch across services | Config type ambiguity |

The mechanism that changed between these two incidents —
canary rollout — is the single biggest process difference, and it shows
directly in both blast radius and duration.

## Note on severity

This is filed as Sev2 rather than Sev1 specifically because the canary
mechanism limited blast radius. Worth remembering when reading old
incident data: not every entry here is a full outage.
