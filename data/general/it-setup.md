---
title: IT and Account Setup
department: general
owner: all
effective: 2026-01-15
summary: Laptop setup, accounts, password manager, VPN and how to request access.
---

# IT and Account Setup

Last updated by: john@nimbuslabs.io (this predates the fuller
`tooling-and-access-requests.md` page — keep this one as the quick
day-1 version, that one as the fuller reference).

## Your accounts

On day 1 you receive a Nimbus Labs email address, Slack, Workday, and
Google Workspace. Engineering staff also get GitHub and cloud console
access. See `tooling-and-access-requests.md` for the full table of what's
automatic by department versus requested separately — this page only
covers the mechanics of account setup, not the full access matrix.

## Password manager

All credentials must be stored in 1Password. Never store credentials in
code, documents, or Slack messages. This is restated more strongly in
`security-policy.md` section 1.1 because it's the most commonly violated
rule in practice, not because the rule itself changed.

## Two-factor authentication

2FA is required on every account. Use the authenticator app, not SMS.
SMS is explicitly disallowed for systems touching customer data or money
— see `security-policy.md` section 1.2 for the reasoning, which mostly
comes down to SIM-swap fraud risk.

## VPN

The VPN is required only for admin consoles and the staging database.
Normal work does not need it. If you're being prompted for VPN
constantly during normal work, something's misconfigured — flag it in
#it-requests rather than assuming it's intentional.

## Requesting extra access

File an access request in the IT Slack channel (#it-requests) with the
system name, the reason, and your manager in the thread. Requests are
reviewed within one working day. Access is granted at the department
level by default.

Note: `tooling-and-access-requests.md` describes an explicit manager
**approval** step (a ✅ reaction or reply) before IT grants anything,
where this page just says requests are "reviewed." In practice the
approval step has always been required — this page is just older and
less precise about it. Follow the newer page if you want the exact
mechanics.

## Quick reference: default accounts by department

| Department | Day-1 accounts |
|---|---|
| Engineering | Email, Slack, Workday, Google Workspace, GitHub, GCP viewer |
| Growth | Email, Slack, Workday, Google Workspace, CRM, Figma viewer |
| People | Email, Slack, Workday, Google Workspace, ATS |
| Finance | Email, Slack, Workday, Google Workspace, accounting system |

## TODO

- This page needs a named owner — right now whoever in Engineering
  notices it's stale fixes it, same situation as
  `tooling-and-access-requests.md` describes for itself.
