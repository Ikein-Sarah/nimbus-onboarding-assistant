---
title: Runbook - Database Failover
department: engineering
owner: all
effective: 2026-06-01
summary: Step-by-step for failing over the primary Postgres instance during a Sev1 or planned maintenance.
---

# Runbook: Database Failover

Last updated by: john@nimbuslabs.io

Use this during a Sev1 database incident (see `oncall-rotation.md` for
severity definitions) or a planned maintenance window announced in the
engineering channel. This is a mechanical checklist, not a diagnostic
guide — if you don't yet know the primary is actually the problem, stop
and diagnose first.

This runbook exists because a database failover is rare enough that
nobody does it often enough to remember the steps reliably under
pressure, and consequential enough that getting a step wrong or out of
order can turn a contained incident into a longer one. Read it end to
end once when you're not in an incident, so the shape of it is familiar
before you ever need to follow it live.

## When to use this runbook

Failover is appropriate when the primary Postgres instance is degraded
or unreachable in a way that a restart, connection pool reset, or query
kill won't fix — hardware-level failure, an unrecoverable disk issue, or
a corruption that's isolated to the primary and not replicated forward.
It is **not** the first thing to try for generic slowness or a spike in
slow queries; those usually mean a bad query plan or lock contention, not
a failed instance, and failing over won't fix either.

| Symptom | Failover appropriate? |
|---|---|
| Primary instance unreachable / connection refused | Yes |
| Primary reports disk or hardware fault in cloud console | Yes |
| Elevated query latency, instance otherwise healthy | No — investigate query plans first |
| Replication lag growing on the standby | No — this is a standby problem, not a primary problem |
| Application-level connection pool exhaustion | No — restart the affected service instead |

## Before you start

- [ ] Confirm you're looking at the primary, not a read replica. Check the
      instance label in the cloud console, not just the connection string
      name (these have drifted out of sync before).
- [ ] If this is a Sev1, make sure the incident is already declared per
      `oncall-rotation.md` before you touch anything. Failovers get
      confusing to reason about after the fact if there's no incident
      timeline.
- [ ] Page the secondary if you haven't already. Do not do a failover
      solo during a live incident.
- [ ] Confirm the standby replica itself is healthy before promoting it —
      promoting an unhealthy standby turns one problem into a worse one.
      Check replication lag in the console; anything under 10 seconds is
      normal, anything over a minute is worth pausing on before
      proceeding.
- [ ] Have the instance IDs for both primary and standby written down
      somewhere visible (a scratch doc, the incident channel) before you
      start issuing commands — under incident pressure, typing the wrong
      instance ID into a promotion command is a real risk.

## Failover steps

1. Announce in #incidents that a failover is starting, with the reason
   and the instance ID. Example: "Starting failover of primary
   `nimbus-prod-pg-01` due to unreachable instance, promoting standby
   `nimbus-prod-pg-standby-01`."
2. Promote the standby replica: `gcloud sql instances promote-replica
   <replica-id>` (use the staging alias to check the command syntax if
   unsure — do not test flags against production). This is a one-way
   operation — once a replica is promoted, it becomes an independent
   primary and can't be demoted back to standby status without a full
   re-setup.
3. Wait for the promotion to report healthy in the console. This
   typically takes 2-5 minutes. Do not proceed early. You can check
   status with `gcloud sql instances describe <replica-id>` and confirm
   `state: RUNNABLE` alongside the instance type showing as primary
   rather than read replica.
4. Update the application's connection secret to point at the newly
   promoted instance. This is a config change through the normal deploy
   pipeline (`deployment-process-v2.md`) — it does **not** skip the
   canary stage, even during an incident, unless the incident lead
   explicitly overrides it and says so in #incidents.
5. Confirm application health checks pass against the new primary.
6. Spin up a new standby replica from the newly-promoted primary, so
   we're not running without redundancy longer than necessary.
7. Announce completion in #incidents with the new instance ID.

## After a failover

- Write or update the incident postmortem within 3 working days per the
  normal rule. Use `incident-postmortem-2026-03-outage.md` as a
  formatting reference if this is your first one.
- Confirm monitoring and alerting are pointed at the new primary — this
  has been missed before and caused a gap in coverage until the next
  business day.
- File a ticket to decommission the old primary once you're confident the
  new one is stable (usually 48 hours).
- Update any runbooks, dashboards, or hardcoded instance references
  (there shouldn't be many, but check) that pointed at the old primary's
  instance ID.
- Let the rest of engineering know in the engineering channel, even for
  a planned maintenance failover — a silent instance ID change can
  confuse someone debugging something unrelated later.

## Common mistakes

- Skipping the "wait for healthy" step and updating the connection secret
  too early, which causes a second round of errors on top of the
  original incident.
- Forgetting the new standby replica step and leaving the system with a
  single point of failure for days.
- Running this against staging thinking it's a low-risk dry run — it
  isn't harmless, staging failovers can knock out data other engineers
  are relying on for testing. Announce staging failovers too.
- Promoting a replica that's lagging significantly behind the primary,
  which can mean losing the most recent writes. This is why the "before
  you start" checklist above has you check replication lag first — a
  failover under time pressure is exactly when this gets skipped.
- Forgetting that failover doesn't fix an application-level bug. If the
  original symptom was caused by bad application code rather than
  instance failure, the same symptom will reappear against the new
  primary.

## Failure modes during the failover itself

| What goes wrong | What to do |
|---|---|
| Promotion command hangs with no status change | Wait up to 10 minutes before assuming it's stuck — some promotions take longer under load. If still hung after 10 minutes, escalate to the engineering lead rather than retrying the command. |
| Application can't connect after the secret update | Confirm the deploy actually completed (check the pipeline, not just that you triggered it) before assuming the new primary itself is unhealthy. |
| New standby replica creation fails | Not urgent — the application is already healthy against the new primary at this point. Retry once, then file a ticket rather than blocking incident closure on it. |
| Health checks fail against the new primary after promotion | Don't roll further — pause and diagnose. A second failover attempted quickly, without understanding why the first one didn't resolve things, tends to make timelines harder to reconstruct afterward. |

## Roles during a failover

For a Sev1-triggered failover specifically, it helps to be explicit
about who's doing what, since this runbook's steps don't all fall to one
person in practice:

| Role | Typically does |
|---|---|
| Primary on-call | Runs the failover steps directly, owns the #incidents announcements |
| Secondary on-call | Confirms standby health independently before promotion, acts as a second check on the instance ID before the promote command runs |
| Engineering lead (if paged per the 2-hour escalation rule) | Makes the call on whether to proceed with failover vs. try further diagnosis, if the situation is ambiguous |

This isn't a rigid assignment — for a planned maintenance failover with
no time pressure, one person can reasonably run the whole thing solo.
It's specifically during a live Sev1 that having a second set of eyes on
the instance ID before promotion matters, per the "before you start"
checklist above.

## Why each step is ordered the way it is

A couple of the ordering choices above aren't arbitrary and are worth
understanding rather than just following mechanically:

- **Announce before promoting, not after.** If the promotion command
  fails or hangs (see the failure modes table below), the team already
  knows a failover is in progress rather than discovering it
  after the fact from an unexplained instance ID change.
- **Wait for healthy before updating the connection secret.** Updating
  the secret first would point the application at an instance that
  might not actually be ready to serve traffic yet, turning a
  controlled failover into a second, self-inflicted outage.
- **Spin up a new standby before decommissioning the old primary.**
  Running without redundancy for the shortest possible window matters
  more than closing out the incident quickly — a second failure with no
  standby available would be a much worse outcome than a slightly longer
  incident timeline.

## Practicing this runbook

Because real failovers are rare, the team runs a practice failover
against staging roughly once a quarter — announced in advance, per the
"announce staging failovers too" rule above. This isn't about the
staging environment itself; it's about keeping the muscle memory for the
actual command sequence fresh so the first time someone runs this for
real isn't also the first time they've run it at all. If you haven't
done a practice run yet, ask in the engineering channel to be looped
into the next one rather than waiting for a real incident to be your
first exposure to these steps.

## Related documents

This runbook is the mechanical companion to
`oncall-rotation.md` (who owns the incident and when to escalate) and
`deployment-process-v2.md` (how the connection secret update actually
gets deployed, canary stage included). None of the three replaces the
others — a real database incident typically involves reading all three.
