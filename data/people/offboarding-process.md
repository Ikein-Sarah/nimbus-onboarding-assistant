---
title: Offboarding Process
department: people
owner: all
effective: 2026-05-10
summary: What happens when someone leaves — access removal, final pay, exit interview and equipment return.
---

# Offboarding Process

Last updated by: tunde@nimbuslabs.io

## Timeline

Offboarding starts the day a departure is confirmed (resignation accepted
or termination decided), not on the person's actual last day.

| When | What |
|---|---|
| Day departure is confirmed | People notifies IT and the manager; last day is set |
| 3+ working days before last day | Manager plans knowledge transfer |
| Last day, morning | Exit interview (voluntary departures only) with People |
| Last day, end of day | All access revoked, equipment collected or shipping label sent |
| Within 5 working days after | Final pay processed, including any unused accrued leave |

## Access removal

This is IT's responsibility to execute, same day as the last day — see
the "Offboarding" section of `general/tooling-and-access-requests.md`
for the request-side pointer. In practice this means:

- Email, Slack, Workday, Google Workspace: disabled end of day.
- Engineering-specific: GitHub, GCP, production DB, PagerDuty access
  pulled same day, not just deactivated-eventually.
- 1Password: account access removed; any shared vaults the person had
  access to should have their credentials rotated within a week if the
  departure wasn't fully amicable — this is a judgment call for the
  manager and People together.

## Equipment

Laptops and any other company equipment (see personal equipment records
for what was issued) are returned via courier with a prepaid label,
arranged by People. If equipment isn't returned within 30 days, Finance
follows up directly — this has only happened a handful of times but it's
Finance's process, not People's, once it gets to that point.

## Final pay

Includes payment for any unused accrued annual leave, per
`general/leave-policy.md`'s accrual rules. Processed within 5 working
days of the last day, separate from the normal payroll cycle timing.

## Exit interviews

Offered to voluntary departures, not typically done for terminations.
Conducted by People, notes kept confidential and used in aggregate for
retention patterns, not shared with the departing employee's manager
individually unless the departing employee explicitly says it's fine.

## What happens to their documents

- Their personal folder is retained per standard data retention (see
  `general/security-policy.md` section 3.3 for the general retention
  principles — offboarded employee personal folders aren't explicitly
  itemized there yet, treat them as retained indefinitely until Legal
  gives different guidance).
- Their access to all department and personal folders ends immediately;
  this happens automatically alongside the account deactivation above,
  not as a separate manual step.

## TODO

- Add a country-specific final pay timing table — the 5-working-day
  target above is the general case, some countries have different legal
  minimums and this doc doesn't capture that yet.
