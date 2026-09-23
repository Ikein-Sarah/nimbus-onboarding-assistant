---
title: Tooling and Access Requests
department: general
owner: all
effective: 2026-07-01
summary: How to request access to a system, who approves it, and the standard tool list by department.
---

# Tooling and Access Requests

Last updated by: john@nimbuslabs.io (this one drifted onto Engineering's
plate because IT doesn't have a dedicated owner yet — see TODO at the
bottom)

This expands on the short "Requesting extra access" section in
`it-setup.md`. That page tells you 2FA and password manager basics; this
page tells you which tool to ask for and roughly how long it takes.

## Standard tools by department

| Department | Tools granted on day 1 | Requested separately |
|---|---|---|
| Engineering | GitHub, GCP console (viewer), Datadog, staging DB read | GCP console (admin), prod DB access, PagerDuty |
| Growth | CRM (Hubspot), Ahrefs, Figma (viewer), ad platform seats | Figma (editor), paid ad account owner |
| People | Workday admin, applicant tracking system, 1Password admin vault | Background check vendor portal |
| Finance | Accounting system, expense tool admin, banking portal (view) | Banking portal (payment initiation) |

## How to request

1. Post in #it-requests with: system name, why you need it, and your
   manager tagged in the thread.
2. Manager reacts with ✅ or replies with a question. No approval, no
   access — silence is not approval.
3. IT (currently: whoever's on the IT rotation that week, check the pinned
   post) grants access within 1 working day of manager approval.

This is slightly different from the old wording in `it-setup.md`, which
says requests are "reviewed within one working day" without mentioning the
manager approval step explicitly. The manager step has always been
required in practice; `it-setup.md` just doesn't spell it out. Follow this
page for the actual process.

## Elevated access (prod DB, banking portal, admin consoles)

These need a second approval beyond your manager:

- Production database write access: Engineering Manager + on the
  `engineering/oncall-rotation.md` rotation, or a documented one-off reason
  approved by the tech lead.
- Banking portal payment initiation: Finance Lead approval, logged in the
  request thread, not just a Slack reaction.
- Customer data exports: see `growth/crm-rules.md` for the growth-specific
  version of this rule.

## Offboarding

Access removal on someone's last day is the manager's responsibility to
kick off, IT's responsibility to execute same day. See
`people/offboarding-process.md` for the full checklist — this page only
covers requesting access, not removing it.

## TODO

- This page needs a real owner. It's been maintained ad hoc by whoever in
  Engineering noticed it was stale. People or IT should probably own it
  going forward since most requests aren't engineering-specific.
- Add SSO details once we migrate off per-tool logins (H2 2026 project,
  not started).
