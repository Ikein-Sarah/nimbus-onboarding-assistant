---
title: Runbook - New Vendor Payment Setup
department: finance
owner: all
effective: 2026-05-01
summary: Step-by-step for onboarding a new vendor and setting up their first payment, from approval through to payment run.
---

# Runbook: New Vendor Payment Setup

Last updated by: lara@nimbuslabs.io, based on the process she shadowed
during her own onboarding per `onboarding-checklist.md`.

Use this once a vendor has cleared the approval step in
`procurement-approvals.md` — this runbook picks up after approval, it
doesn't cover getting the spend approved in the first place.

## Before you start

Confirm you actually have an approved request to work from, not just a
verbal "go ahead." The approval matrix in `procurement-approvals.md` is
specific about who can approve at each contract value — if you can't
point to who approved it and at what value, pause and get that
confirmed in writing (a Slack approval in the request thread counts)
before doing anything else in this runbook.

| Contract value | Confirm approval from |
|---|---|
| Up to 1,000 USD | Requester's manager |
| 1,001 - 5,000 USD | Department lead |
| 5,001 - 25,000 USD | Henrik (Finance lead) |
| Above 25,000 USD | Henrik and the CEO |

## Steps

1. **Collect vendor form and tax details.** Required before anything else
   per `procurement-approvals.md`'s "New vendors" section. Missing tax
   details is the single most common reason this stalls.
2. **Determine if a security review is needed.** If the vendor will
   process customer data, loop in whoever's handling security review that
   quarter (see `general/security-policy.md` section 4 for the general
   principle — this runbook is the finance-side execution of that rule).
   Do not skip this because the deal is small; deal size and data
   sensitivity aren't correlated.
3. **Set contract terms.** Default is 12 months, net 30 payment terms.
   Anything shorter than net 30 needs Henrik's approval per
   `procurement-approvals.md`. Flag any auto-renewal clause explicitly in
   the contract record — these get missed and cause surprise renewals.
4. **Create the vendor record** in the accounting system with the agreed
   terms.
5. **Set up the payment method.** Bank transfer is default; card payment
   for recurring SaaS under 1,000 USD/year is acceptable without
   additional approval.
6. **Schedule the first payment** according to the invoice due date and
   the agreed terms. Don't pay early "to be safe" — early payment on net
   30 terms distorts the monthly cash forecast in `budget-planning.md`.
7. **Confirm with the requesting department** that the vendor is live and
   who their point of contact is going forward.

### Worked example

A Growth team member wants to onboard a new ad-platform data vendor at
8,000 USD/year. Walking through the steps: this falls in the 5,001-25,000
USD band, so it needs Henrik's approval per `procurement-approvals.md`
before this runbook starts. Once approved, because this vendor will
process customer targeting data, step 2's security review is mandatory
regardless of the moderate deal size. Contract terms default to 12
months net 30 unless negotiated otherwise. Because it's a recurring
subscription, step 5's payment setup should use the recurring payment
path described below, not a one-off manual entry each billing cycle.

## Recurring vs. one-off vendors

For recurring vendors (subscriptions, retainers), set up the payment as
recurring in the accounting system from the start rather than re-entering
it every month — re-entry is where most of the reconciliation errors in
the monthly close come from.

### Setting up a recurring payment

1. In the accounting system's vendor record, mark the payment as
   recurring rather than one-off — this is a checkbox on the vendor
   record, not a separate payment entity.
2. Set the cadence (monthly, quarterly, annual) to match the invoice
   terms actually agreed, not just a default guess.
3. Set an expected amount. If the vendor's charges vary (usage-based
   pricing, for example), set a reasonable estimate and flag the record
   as variable so reconciliation doesn't treat every difference as an
   error.
4. Set a review reminder for contract renewal — 60 days before the
   default 12-month term ends, so an auto-renewal clause (flagged in
   step 3 of the main steps above) doesn't surprise anyone.

### One-off vendors

For genuinely one-time purchases, a recurring setup is unnecessary
overhead — just process the single payment against the vendor record
and don't create a recurring schedule. If a "one-off" vendor turns out
to need a second payment later, convert the record to recurring at that
point rather than leaving it as a series of disconnected one-off
entries, which is harder to reconcile against forecasted spend in
`budget-planning.md`.

## If a payment fails

- Confirm the banking portal shows the failure reason before retrying
  blind.
- If it's a payment initiation permissions issue, that's a
  `general/tooling-and-access-requests.md` access problem, not a vendor
  problem — check who actually has payment initiation rights before
  assuming the vendor's bank details are wrong.
- Retried payments still need to land inside whatever payment terms were
  agreed — a failed and retried net 30 payment doesn't get a grace
  period extension automatically.

## Closing out a vendor relationship

Not covered in detail here yet — if a vendor is being terminated rather
than onboarded, talk to Henrik directly. This runbook is onboarding-only
for now; offboarding a vendor will get its own doc once we've done it
enough times to have a stable process (currently ad hoc).

## Failure modes and what to do

| What goes wrong | What to do |
|---|---|
| Vendor form is incomplete (missing tax details) | Don't create the vendor record yet — an incomplete record causes payment failures later that are harder to trace back to the root cause. Chase the missing details first. |
| Security review flags a concern | Pause the vendor setup entirely until it's resolved with whoever ran the review — don't proceed "provisionally" while waiting, even under time pressure from the requesting department. |
| Requester wants payment terms shorter than net 30 | Requires Henrik's explicit approval per `procurement-approvals.md`, not just a note in the vendor record — get it in writing in the request thread. |
| Vendor's bank details look unusual or were sent via an unsolicited channel | Treat as a potential fraud attempt per `general/security-policy.md` section 5 — verify independently through a known contact at the vendor, don't just proceed. |
| Recurring payment set up as one-off by mistake | Fix before the second billing cycle — re-entry errors like this are the most common source of reconciliation problems in the monthly close, per the note below. |

## A note on recurring vendors specifically

The reconciliation problems mentioned above are disproportionately
caused by recurring vendors that were set up as one-off payments and
then manually re-entered each cycle, sometimes with slightly different
amounts due to typos or a missed price change. Setting up the payment
as genuinely recurring in the accounting system from day one, per step 5
above, avoids nearly all of this — it's a small amount of extra setup
effort that pays for itself within two or three billing cycles.

## How this fits into the monthly close

Finance's monthly close process (not documented in its own runbook yet)
relies on vendor records being accurate and complete by a set cutoff
each month. A vendor onboarded correctly per this runbook, with a proper
recurring schedule rather than manual re-entry, essentially takes care
of itself each month — it's already the kind of record the close process
expects. A vendor onboarded sloppily (missing terms, one-off entries for
what's actually a recurring charge) becomes a recurring source of
manual reconciliation work every single month, not just a one-time
inconvenience. This is the main reason this runbook cares as much as it
does about getting the setup right the first time rather than treating
"vendor is technically paid" as good enough.

## What "done" looks like

It's easy to lose track of whether a vendor setup is actually complete
versus just "mostly done." A vendor onboarding is finished when all of
the following are true, not when the first payment has merely been
scheduled:

- [ ] Vendor record exists in the accounting system with correct terms
- [ ] Tax details are on file, not just requested
- [ ] Security review is either completed (if required) or explicitly
      marked not-required, not just skipped silently
- [ ] Payment method is set up and tested with the first real payment
- [ ] Recurring schedule is configured, if applicable, per the section
      below — not left as a manual monthly re-entry
- [ ] Requesting department has confirmed the vendor is live and knows
      their point of contact
- [ ] Auto-renewal clause, if any, has a review reminder set

A vendor missing any of these isn't "basically done" — it's a partial
setup that will eventually cause a problem, usually at the worst time
(a renewal nobody flagged, a payment that fails because tax details were
never actually collected).

## Why the steps are ordered this way

Tax details and the security review (steps 1-2) come before contract
terms and the vendor record (steps 3-4) deliberately — both are the
slowest parts of the process when they're needed, and starting them
early means they run in parallel with the rest of the setup rather than
blocking it at the end. Finance hires sometimes try to set up the
vendor record first and circle back for tax details later, which feels
faster but usually isn't: an incomplete vendor record can't have a
payment scheduled against it anyway, so nothing is actually saved by
reordering, and it's easier to lose track of a half-completed record
than an explicitly pending task.

## Common questions from new Finance hires

**What if the requesting department wants the vendor live faster than
this process allows?** The approval steps (per `procurement-approvals.md`)
aren't something this runbook can shortcut — but within the runbook
itself, the fastest path is having a complete vendor form and tax
details ready on day one, since that's the most common source of delay,
not the runbook's own steps.

**What if I'm not sure whether a vendor needs a security review?** Ask
whoever's handling security review that quarter rather than guessing —
guessing wrong in the direction of "probably doesn't need one" is the
riskier mistake, per `general/security-policy.md` section 4.

**Can I set up a vendor before the approval is fully confirmed, to save
time?** No — see "Before you start" above. This has caused rework before
when an approval came back different from what was assumed.

## Related documents

This runbook is the execution-side companion to
`procurement-approvals.md` (the approval rules) and
`onboarding-checklist.md`'s Week 2 shadowing exercise for new Finance
hires. `general/security-policy.md` section 4 covers the general
principle behind step 2's security review requirement.
