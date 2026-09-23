---
title: Architecture Overview
department: engineering
owner: all
effective: 2026-07-15
summary: How Nimbus Flow is put together — services, data stores, queues, and how they talk to each other.
---

# Architecture Overview

Last updated by: john@nimbuslabs.io, in his tech-lead capacity rather
than as a day-to-day contributor doc.

This is the long-form reference for how the platform actually fits
together. If you just need to get a local environment running, use
`dev-environment-setup.md` instead — this doc is for understanding why
things are shaped the way they are, not for day-1 setup.

## 1. The big picture

Nimbus Flow is a monolith-with-workers architecture, not microservices.
This is a deliberate choice, not a historical accident we haven't gotten
around to fixing — at our scale (mid-sized logistics customers, not
consumer-scale traffic), the coordination overhead of microservices
wasn't worth it, and we've revisited the decision twice without
changing our minds.

```
                    ┌─────────────┐
   customer <──────>│   API (8000) │<──────> Postgres (primary)
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │    Redis    │  (queues + cache)
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │   Worker    │<──────> Postgres (read replica)
                    └─────────────┘
```

## 2. The API

A single Django-style monolith (internal framework, not literally
Django) serving both the customer-facing product and the internal admin
tools. Organized into modules by domain (dispatch, billing, users,
integrations) rather than by technical layer — this mirrors the
company's department structure more than it mirrors a typical MVC split,
which occasionally confuses engineers coming from more layered
codebases.

### Modules, briefly

| Module | Roughly covers |
|---|---|
| dispatch | The core scheduling logic — Nimbus Flow's original purpose |
| billing | Invoicing, payment processing, the worker-side reconciliation described in section 3 |
| users | Accounts, auth, permissions — including the admin tool's own role system, see section 7 |
| integrations | Inbound REST API and outbound webhook handling, see section 6 |

### Authentication and billing

These two modules require two-approval code review per
`code-review-guidelines.md` and a feature flag under
`deployment-process-v2.md`. This isn't arbitrary caution — both modules
have caused real incidents historically, including the one described in
`incident-postmortem-2026-03-outage.md`, which was a billing-adjacent
schema change.

### A request's life cycle, roughly

Useful to have in mind when debugging: a typical customer request
(say, updating a dispatch record) hits the API, which authenticates the
request against the users module, executes the dispatch logic against
Postgres primary, and — if the change has downstream effects (a webhook
needs to fire, a billing event needs to be recorded) — pushes a job onto
a Redis queue rather than doing that work synchronously. The API
responds to the customer before the worker has necessarily finished
processing that job. This is why a successful API response doesn't
always mean every downstream effect has completed yet — most of the
time this gap is milliseconds and invisible, but it matters when
debugging something that depends on a webhook or invoice having already
fired.

## 3. The worker

Background job processing: emails, scheduled dispatch calculations,
webhook delivery to customer systems, and the async parts of billing
(invoice generation, payment reconciliation). Pulls from Redis-backed
queues. The July canary rollback
(`incident-postmortem-2026-07-deploy-rollback.md`) was a worker-side
bug, which is part of why worker changes get particular scrutiny in
review even though the formal two-approval rule is scoped to auth,
billing, and deletion rather than "anything in the worker."

## 4. Data stores

### Postgres (primary)

Single primary, single standby (see `runbook-database-failover.md` for
what happens when this needs to change). All writes go here. Schema
migrations follow the backward-compatibility rule in
`deployment-process-v2.md` — migrations must work with both the old and
new application code for at least one release, because code and schema
deploy on separate pipelines.

### Postgres (read replica)

Used by the worker and by reporting queries that would otherwise put
load on the primary during customer-facing traffic. Slight replication
lag (typically under a second, occasionally more under load) means the
worker should never assume read-after-write consistency against the
replica.

### Redis

Two purposes that share one instance today, which is a known
simplification we'd like to undo eventually: job queues for the worker,
and a cache layer for a handful of expensive API reads. If Redis needs a
failover, both purposes go down together — there's no runbook for this
yet, unlike the database failover runbook, because it hasn't happened in
production so far.

## 5. Environments

Matches `dev-environment-setup.md` and `deployment-process-v2.md`:
local, staging, production. Staging is a scaled-down mirror of
production's architecture — same services, same relationships, smaller
instance sizes, and it does not have the read replica (reporting queries
hit the single staging Postgres instance directly).

## 6. External integrations

Nimbus Flow integrates with customers' existing systems via webhooks
(outbound, from the worker) and a REST API (inbound). Integration-related
incidents are usually Sev2 rather than Sev1 by the definitions in
`oncall-rotation.md`, since a broken integration for one customer is
"customer facing and partial," not total — unless it's a widespread
integration failure affecting many customers simultaneously, which would
escalate.

Outbound webhooks retry on failure with backoff, up to a bounded number
of attempts, after which a failed delivery is logged and surfaced to the
customer's integration dashboard rather than retried indefinitely — an
indefinitely retrying webhook against a permanently broken customer
endpoint would otherwise slowly consume worker capacity meant for
everyone else, which is exactly the kind of coupling section 3 warns
about.

## 7. Scaling notes

Nimbus Flow's traffic profile is business-hours-heavy and spread across
customer time zones rather than having a single sharp daily peak — a
side effect of the customer base being logistics companies with their
own regional working hours. This means capacity planning looks more like
"handle a rolling wave across time zones" than "handle one big spike,"
which has shaped a few decisions:

- The API scales horizontally behind a load balancer; individual
  instances are stateless, so scaling out is straightforward.
- The worker scales similarly, though queue depth (not CPU) is usually
  the trigger for adding worker capacity — a growing queue backlog is
  the earliest visible sign of the worker falling behind.
- Postgres primary is the hardest part of the system to scale
  horizontally, which is part of why the read replica exists — moving
  read-heavy work off the primary buys headroom without a harder
  architectural change.

## 8. What's NOT covered here

- Frontend architecture — ask in the engineering channel, it doesn't
  have a written doc yet.
- The internal admin tool's permission model — related to but distinct
  from the document access rules in `general/employee-handbook.md`; the
  admin tool has its own role system that predates and doesn't map
  cleanly onto department-based document access.
- Infrastructure-as-code / Terraform layout — exists, just not
  documented at this level yet.

## 8a. Observability

Datadog is the primary tool for both metrics and logs — see
`oncall-rotation.md` and the canary-specific alerting described in
`incident-postmortem-2026-07-deploy-rollback.md` for how this feeds
into incident detection. A few things worth knowing:

- API and worker both emit structured logs tagged by module (dispatch,
  billing, users, integrations), which makes it possible to filter logs
  by the module breakdown in section 2 even though they run as parts of
  the same deployed monolith.
- The canary tag on metrics (introduced with `deployment-process-v2.md`)
  lets you filter any dashboard down to just canary traffic, which is
  useful beyond incident response — it's also how engineers manually
  sanity-check a canary before promoting it, not just relying on the
  automatic threshold check.
- There's no centralized tracing across the API → Redis → worker path
  yet. Debugging a request that crosses that boundary currently means
  correlating logs by a shared request ID manually, which is slower than
  it should be — a known gap, not a design choice.

## 7a. What breaks first under load

If you're trying to build intuition for where the system is fragile,
the rough order in which components show strain as load increases has
historically been: Postgres primary write throughput first, worker queue
depth second (usually a lagging indicator of the first, since a slow
primary means slower job completion), then Redis memory pressure a
distant third since job payloads are small. API instance CPU has never
been the bottleneck in practice — the API spends most of its time
waiting on Postgres, not computing. This ordering isn't written down
formally anywhere else, it's institutional knowledge from a handful of
past incidents including the two described in this corpus's postmortems.

## 8b. Why monolith-with-workers, revisited

Section 1 mentions this decision has been revisited twice without
changing. Worth saying a bit more about why, since it's a common
question from engineers who've worked in more microservice-heavy
environments before:

- **Team size.** With engineering at roughly 35 people company-wide,
  splitting into many independently-deployed services would mean each
  service having very few owners — below the threshold where the
  independence benefits of microservices usually outweigh the
  coordination cost of many deploy pipelines, many sets of dashboards,
  and many places a cross-cutting change has to be made.
- **Traffic shape.** Section 7's scaling notes describe a rolling,
  time-zone-spread load rather than one component needing to scale far
  beyond the others — one of the more common reasons to split out a
  service (isolating a hot path) doesn't apply strongly here.
- **What we'd actually gain.** The honest case for splitting further is
  mostly about deploy independence — being able to ship the worker
  without redeploying the API, for instance. The canary and feature-flag
  mechanisms in `deployment-process-v2.md` capture a meaningful chunk of
  that benefit already, without the operational overhead of a full
  service split.

This could change as the company grows — the decision has been described
as "not yet worth it," not "never worth it."

## 9. Why this matters for on-call

If you're on the rotation (`oncall-rotation.md`), the mental model above
is the fastest way to guess where an incident lives: customer-facing and
immediate usually means API or Postgres primary; delayed or
integration-related usually means worker or Redis queue backlog. This
isn't a substitute for the actual escalation and runbook docs, just a
faster first guess.

## TODO

- Add a real diagram once we're not relying on ASCII art (same TODO as
  `general/org-chart.md`, different diagram).
- Document the admin tool permission model referenced in section 7.
