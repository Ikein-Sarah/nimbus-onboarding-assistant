---
title: New Joiner FAQ
department: general
owner: all
effective: 2026-06-01
summary: Informal answers to the questions new joiners actually ask in their first month.
---

# New Joiner FAQ

Last updated by: tunde@nimbuslabs.io. Written informally on purpose —
this is the "ask a friendly coworker" page, not a policy doc. If you want
the formal version of an answer, follow the link.

## "Do we have stock options / equity?"

No. Nimbus Labs does not currently offer equity or stock options to
employees. This comes up a lot, especially from engineering candidates
coming from bigger tech companies, so it's worth saying plainly: it's not
a documentation gap, it's genuinely not a thing we offer right now.

## "What about a pension or retirement plan?"

We don't run a company pension scheme. Depending on your country of
employment there may be a statutory scheme your payroll contributes to
automatically (this varies by country), but there's no Nimbus Labs
pension program on top of that. Ask Finance if you want the specifics for
your country — but there's no internal doc that covers this in general
terms because it's not a unified policy, it's just "whatever your country
requires."

## "Can you tell me the company's revenue / how we're doing financially?"

Not published internally at the detail level. Budget envelopes and
headcount plans are visible to Finance and relevant department leads (see
`finance/budget-planning.md`), but top-line revenue numbers aren't shared
company-wide. If leadership shares something in an all-hands, that's the
extent of it.

## "I got an email that looks like phishing, what do I do?"

Don't click anything. Forward it or screenshot it into
#security-incidents. See `security-policy.md` section 5 for the full
process — but honestly, just reporting it is 90% of what matters, the
process document is for the harder cases.

## "How do I expense something?"

Short version: keep the receipt, submit within 30 days, check
`finance/expense-policy.md` for the limits. If it's under the
no-pre-approval limits (software under 50 USD/month, meals under 40 USD,
taxis under 30 USD), just submit it. Anything bigger, ask your manager
first informally before submitting.

## "Who approves my leave if my manager is out?"

Their manager, one level up. Check `org-chart.md` if you're not sure who
that is.

## "What's the deal with anchor days, do I have to go to an office?"

No mandatory office days company-wide. If your team has 3+ people in the
same city, you'll probably land on one shared day a week — that's a team
decision, not something imposed from above. See `hybrid-work-policy.md`.

## "Someone told me the old remote work policy said something different"

They're right, and the old one (`remote-work-policy.md`) is archived now.
`hybrid-work-policy.md` is current as of 2026-08-15.

## "Can I see someone else's salary / offer / review?"

No. Not even someone on your own team, not even your manager's, unless
you're their manager or in People. This one comes up more than you'd
think — the access boundaries in `employee-handbook.md` ("Document
access") are real, not just a formality.

## "What does 'ICP' mean, I keep seeing it in Growth Slack"

Ideal customer profile. See `glossary.md` for this and a bunch of other
acronyms.

## "I broke something in production, what now?"

Don't panic-fix it alone if it's serious. See
`engineering/oncall-rotation.md` for severity levels and escalation. If
you're not sure if it's serious, treat it as Sev2 and let the on-call
engineer downgrade it.
