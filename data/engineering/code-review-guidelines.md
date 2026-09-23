---
title: Code Review Guidelines
department: engineering
owner: all
effective: 2025-11-01
summary: What reviewers look for, review turnaround expectations and merge rules.
---

# Code Review Guidelines

Last updated by: daniel@nimbuslabs.io

## Review turnaround

First review within one working day. If you cannot review in that time,
say so in the pull request so the author can find someone else. Don't
just go quiet — a "can't get to this until tomorrow" comment takes 10
seconds and saves the author from waiting blind.

## What reviewers check

Correctness first, then tests, then readability. Style is handled by the
formatter and should not be discussed in review — if the formatter
allows something you personally dislike stylistically, that's a
formatter config conversation, not a review comment on someone's PR.

## Pull request size

Aim for under 400 changed lines. Large changes should be split, or
reviewed in a call rather than in comments. `paid-media-policy.md`'s
kill-switch requirement is unrelated but shows the same instinct in a
different department: big, hard-to-reason-about changes need an extra
safety mechanism, whether that's a smaller diff or a documented rollback
path.

## Merge rules

| Change touches | Approvals required |
|---|---|
| Most things | 1 |
| Authentication | 2 |
| Billing | 2 |
| Data deletion | 2 |

These are the same three categories that require a feature flag under
`deployment-process-v2.md` — if it needs two reviewers here, it needs a
flag there too. Treat the two rules as one boundary, not two separate
lists to remember.

## Disagreements

If author and reviewer cannot agree within two rounds, escalate to the
tech lead (John Adeyemi, currently) rather than continuing in comments.
Escalating isn't a failure — long comment threads rarely converge faster
than a 10-minute call would.

## A note on the March incident

The outage in `incident-postmortem-2026-03-outage.md` passed code review
under these same rules — the review process worked as intended (one
approval, correctness checked), the gap was entirely in deployment
(no gradual rollout), not review. Worth remembering when reading that
postmortem: it's not a review-process failure, it's a deploy-process one.
