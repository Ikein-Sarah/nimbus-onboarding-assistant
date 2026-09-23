---
title: On-Call Rotation and Incident Response
department: engineering
owner: all
effective: 2026-05-01
summary: On-call schedule, severity levels, escalation path and incident reviews.
---

# On-Call Rotation and Incident Response

Last updated by: daniel@nimbuslabs.io. This is one of the longer docs in
Engineering on purpose — getting incident response wrong is expensive, so
this page tries to leave less to memory than most.

## Rotation

On-call runs one week at a time, Monday 10:00 to Monday 10:00, in the
on-call engineer's local time zone. New engineers join the rotation after
their first 90 days, shadowing for one full week first (see
`onboarding-checklist.md`).

There are two roles on the rotation each week:

- **Primary** — first to be paged, owns the response until resolved or
  escalated.
- **Secondary** — backup, paged if primary doesn't acknowledge or asks
  for help.

The rotation currently covers the core platform team (roughly a dozen
engineers company-wide, not just the three in the demo roster). Rotation
order is generated automatically and posted at the start of each quarter
in the engineering Slack channel; this doc doesn't try to keep a live
copy of the schedule since it would drift immediately.

### Swaps

You can swap your week with a teammate at any time — just make sure both
of you post the swap in the engineering channel so the paging tool gets
updated. An unposted swap means pages go to the wrong person, which has
happened, and it is not fun for anyone involved.

## Severity levels

| Severity | Definition | Ack target (in-window) | Handled |
|---|---|---|---|
| Sev1 | Customer facing and total (e.g. checkout fully down) | 15 minutes | Immediately, all hands if needed |
| Sev2 | Customer facing and partial (e.g. one feature degraded) | 60 minutes | Immediately, primary + secondary |
| Sev3 | Internal only, no customer impact | Next working day | During working hours |

A good rule of thumb when you're not sure which severity applies: if a
customer would notice right now, it's at least Sev2. If you're unsure
between Sev1 and Sev2, treat it as Sev1 and let it get downgraded — the
cost of over-declaring is much lower than under-declaring.

## Response expectations

Acknowledge Sev1 within 15 minutes and Sev2 within 60 minutes during the
on-call window. Sev3 is handled the next working day. "Acknowledge" means
you've seen the page and are actively looking, not that the issue is
resolved.

## Escalation

If you cannot make progress in 30 minutes, page the secondary. If the
incident is still open after 2 hours, page the engineering lead (Daniel
Owusu). For anything that looks like a security issue rather than a
plain availability issue, stop and go to `general/security-policy.md`
section 5 instead — that's a different process with a different channel
(#security-incidents, not the incident channel), and starts over from
the beginning rather than escalating through this ladder.

A database-specific incident usually means following
`runbook-database-failover.md` alongside this escalation ladder, not
instead of it — the runbook is the mechanical steps, this doc is the
communication and ownership rules around them.

## After an incident

Write an incident review within 3 working days. Reviews are blameless and
are shared with the whole engineering department. See
`incident-postmortem-2026-03-outage.md` and
`incident-postmortem-2026-07-deploy-rollback.md` for real examples of the
format — use those as templates rather than starting from a blank page.

A blameless review focuses on what happened and what allowed it to happen
(process gaps, missing tests, missing alerting), not on relitigating who
made the call at 2am. This is company culture, not just an engineering
quirk — see the "Blameless, not consequence-free" value in
`general/employee-handbook.md`.

## On-call compensation

On-call weeks are compensated. The rate is set by Finance and appears in
your personal compensation record — this is intentionally not published
here or in any department-wide doc, because it can vary by level and
sometimes by region. If you're on the rotation and unsure what you're
paid for an on-call week, check your personal folder rather than asking a
teammate; theirs may legitimately be a different number than yours.

## Quick reference: who to page for what

| Situation | Page |
|---|---|
| Any Sev1 or Sev2 | Primary on-call (auto-paged) |
| No progress after 30 min | Secondary on-call |
| Still open after 2 hours | Engineering lead (Daniel) |
| Database-specific | Primary + `runbook-database-failover.md` |
| Looks like a security incident | Skip this ladder entirely, go to `general/security-policy.md` |

