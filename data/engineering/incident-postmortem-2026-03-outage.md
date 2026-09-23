---
title: Incident Postmortem - 2026-03-18 Production Outage
department: engineering
owner: all
effective: 2026-03-21
summary: Sev1 outage, full checkout flow down for 42 minutes. Root cause and the action item that led to canary deploys.
---

# Incident Postmortem: 2026-03-18 Production Outage

Written by: daniel@nimbuslabs.io. Reviewed blameless per
`oncall-rotation.md`'s "After an incident" section — this postmortem is an
example of that process in action, not a special case.

## Summary

Sev1. The checkout/billing flow was completely down for 42 minutes
(10:07-10:49 local). Root cause was a schema change deployed to 100% of
production traffic at once, with no gradual rollout, that broke a
downstream billing worker still expecting the old schema.

## Impact

- **Customer facing:** checkout was completely unusable for the full 42
  minutes. Any customer attempting to complete a booking or trigger a
  billed action during that window saw a failure page.
- **Scope:** all customers on the platform, since checkout runs through a
  single shared code path — there's no per-customer isolation at this
  layer (see `engineering/architecture-overview.md` section 2 for why the
  API is structured this way).
- **Data impact:** none. No data was lost or corrupted — the billing
  worker crash-looped rather than writing bad data, which is the
  better of the two ways this kind of schema mismatch can fail.
- **Support load:** 11 support tickets referencing checkout failures came
  in during and shortly after the window, all resolved with a standard
  "known issue, resolved" response once the rollback completed.

## Timeline

- 09:40 — PR #2281 (billing schema migration) merges after one approval,
  green CI, per the merge rules in force at the time
  (`code-review-guidelines.md`).
- 10:04 — Deploy of PR #2281 completes, goes live to 100% of traffic
  immediately — this was standard practice under
  `deployment-process.md` at the time, which had no staged rollout step.
- 10:07 — Error rate alert fires in Datadog. On-call engineer (not named
  here per the blameless format) acknowledges within 4 minutes.
- 10:09 — Initial triage begins; checkout errors confirmed to correlate
  with the 10:04 deploy.
- 10:12 — Sev1 declared, checkout confirmed fully down per the severity
  definitions in `oncall-rotation.md`.
- 10:15 — Secondary paged per escalation rules in `oncall-rotation.md`.
- 10:18 — Primary and secondary confirm the billing worker is
  crash-looping, not the API itself — narrows the search.
- 10:22 — Root cause identified: billing worker deserializing the old
  schema shape, crash-looping on the new one.
- 10:25 — Decision made to roll back rather than forward-fix, given the
  root cause was understood but a targeted fix would take longer to
  write and test safely than a rollback.
- 10:31 — Rollback triggered against the previous deploy tag.
- 10:38 — Rollback deploy completes; worker crash loop stops.
- 10:44 — Error rates return to baseline; checkout confirmed processing
  test transactions successfully.
- 10:49 — Checkout confirmed working again for real traffic. Incident
  closed.
- 10:52 — Incident channel notified, #general posted a short all-clear
  note per standard practice (not written down anywhere formally, just
  what's always been done).

## Root cause

The migration itself was backward compatible at the database level (per
`deployment-process.md`'s migration rule), but the **application code**
deploy that started reading the new schema went to 100% of traffic in one
step. There was no intermediate stage where a small slice of traffic hit
the new code path first. A single-digit-percentage rollout would have
caught the billing worker mismatch in minutes, against a fraction of
customers, instead of full production.

### Why the pre-deploy tests didn't catch it

The main API's test suite covered the new schema shape thoroughly. The
billing worker, which is a separate process consuming from the same
underlying tables (see `architecture-overview.md` section 3), has its own
narrower test suite that hadn't been updated to cover the new shape. This
is a common failure pattern in a monolith-with-workers architecture:
schema changes are easy to test against the code that changed, and easy
to miss against code elsewhere that implicitly depends on the same data
shape.

### Contributing factors, not just the single root cause

- The PR reviewer approved based on the API changes looking correct —
  reasonable, since reviewing for worker-side implications wasn't an
  explicit checklist item anywhere at the time.
- There was no automated check cross-referencing schema changes against
  all known consumers of a table, worker included.

## What went well

- Alerting caught it in under 3 minutes, well inside the tooling's
  design target.
- Escalation path worked exactly as documented — secondary was paged
  within the 30-minute window without anyone needing to think about the
  process live, which is exactly what a good escalation ladder is
  supposed to buy you during a stressful incident.
- Rollback took under 10 minutes once root cause was clear, validating
  that the rollback mechanism in `deployment-process.md` (tag-based,
  no-approval-needed) was fast enough even under pressure.
- Nobody debated whether to declare Sev1. The severity definitions in
  `oncall-rotation.md` made that call unambiguous.

## What went wrong

- No gradual rollout mechanism existed at all. This wasn't a process
  violation — the process simply didn't have a canary step to violate.
- The billing worker's schema assumptions weren't covered by the
  pre-deploy test suite the way the main API's were.
- Root cause took 18 minutes to identify (10:04 to 10:22) — reasonable,
  but slower than it needed to be because the on-call engineer's first
  instinct was to check the API logs rather than the worker logs, since
  checkout errors usually do point to the API.
- No one on the response team had touched the billing worker's
  deserialization code recently, which slowed the "is this actually the
  schema" hypothesis from forming faster.

## Customer communication

Because the outage lasted under an hour and was resolved before most
customers would have escalated to their own support contacts, no
proactive customer-facing communication went out beyond the standard
status page update. This was a judgment call at the time, not a fixed
threshold — for a longer outage, `general/security-policy.md` section 6's
principle (Legal and the CEO loop in before customer comms) would apply
by analogy even though that section is written for security incidents
specifically.

## Action items

| Action | Owner | Status |
|---|---|---|
| Add canary rollout stage to the deploy pipeline | daniel@nimbuslabs.io | Done — see `deployment-process-v2.md` |
| Add schema-compat test for the billing worker specifically | john@nimbuslabs.io | Done |
| Require feature flags for auth/billing/deletion changes | daniel@nimbuslabs.io | Done — part of v2 process |
| Audit other workers for similar implicit schema coupling | john@nimbuslabs.io | In progress, see follow-up postmortem note below |
| Add "check downstream consumers" to the PR template for schema changes | john@nimbuslabs.io | Done |
| Review whether the billing worker should move to a stricter typed schema library | daniel@nimbuslabs.io | Open, not scheduled |

The last item is explicitly not scheduled — it's a larger structural
change than the immediate fixes above, and the team decided the canary
rollout plus the schema-compat test closed the practical risk well
enough to not need it urgently. Worth revisiting if a similar incident
happens again despite the canary stage.

## What a reader should take away from this document

If you're new to Engineering and this is the first postmortem you've
read, the main things worth internalizing aren't the specific timeline
or the specific bug — they're the shape of the response: alert fires,
severity gets declared quickly using clear criteria
(`oncall-rotation.md`), escalation follows a predetermined ladder rather
than improvised decision-making, and the fix (rollback) is decoupled
from the full understanding of root cause (which came later). You don't
need to fully understand why something broke before you can safely
undo it — that's a deliberate design property of the rollback mechanism
in `deployment-process.md`/`deployment-process-v2.md`, not an accident of
how this particular incident played out.

## Why a canary alone wouldn't have been enough, in hindsight

Worth noting for anyone reading this after `deployment-process-v2.md`
was already in place for a while: the canary rollout fixes the "100% of
traffic at once" half of this incident, but the schema-compat test gap
was a separate, independent problem. If the canary stage had existed at
the time without the schema-compat test action item also being done, a
canary deploy of the same bad change would likely have still caused a
Sev1-equivalent failure — just scoped to 5% of traffic instead of 100%,
more like the July incident's severity than March's. Both fixes mattered
independently; neither alone would have fully closed the gap this
incident exposed.

## How this compares to a near-miss the same quarter

Roughly six weeks before this outage, a similar schema change to a
lower-traffic module (internal reporting, not customer-facing) caused a
brief spike in error logs that was noticed and fixed within minutes,
without ever reaching incident status. In hindsight, that near-miss was
an early warning sign of the same underlying gap — no gradual rollout
mechanism — but because it didn't cause visible customer impact, it
wasn't escalated into a broader review of the deploy process at the
time. Worth naming explicitly: the gap this postmortem's action items
closed had already shown itself once before this incident, just not
loudly enough to prompt action on its own.

## Lessons for the broader org

Two things came out of this that went beyond engineering:

1. **Support** didn't have a fast way to know "this is a known incident,
   don't escalate individually" until about 15 minutes into the outage.
   That gap is now closed by the incident channel auto-posting a summary
   that Support can quote directly.
2. This postmortem itself became the template other incident and
   security writeups reference — see
   `general/security-policy.md` section 6, which points here explicitly
   for its own postmortem format.

## Follow-up

The audit in the last action item surfaced a second, unrelated issue that
led to the July deploy rollback — see
`incident-postmortem-2026-07-deploy-rollback.md`. Different root cause,
same general theme of insufficiently isolated rollout.
