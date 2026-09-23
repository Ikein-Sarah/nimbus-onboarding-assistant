---
title: CRM Hygiene and Customer Data Rules
department: growth
owner: all
effective: 2026-04-01
summary: How customer records are created, updated and handled in the CRM.
---

# CRM Hygiene and Customer Data Rules

Last updated by: amaka@nimbuslabs.io

## Record ownership

Every account has exactly one owner. Transfers are done in the CRM, not
by informal agreement — an owner change mentioned in Slack but not
updated in the CRM record doesn't count, and reporting will still credit
the old owner.

## Required fields

Company name, industry, employee count, source, and stage. Records
missing required fields are excluded from reporting.

| Field | Where it's used |
|---|---|
| Industry | Segmentation for campaign targeting |
| Employee count | Rough proxy for our ICP fit (mid-sized logistics) |
| Source | Attribution, feeds into CAC calculations |
| Stage | Pipeline reporting |

## Customer data handling

Do not export customer lists to personal drives or spreadsheets outside
the CRM. Exports for analysis must stay in the company workspace. This is
restated more broadly (covering all departments, not just Growth) in
`general/security-policy.md` section 3.1 — that section exists because
Engineering and Finance also touch customer data sometimes, not just
Growth, and the same boundary should hold everywhere.

## Deletion requests

A customer deletion request is forwarded to the People and Finance teams
the same day it is received, and completed within 30 days. This matches
the general retention principle in `general/security-policy.md` section
3.3 — this document is the Growth-specific execution of that rule since
Growth is usually where the request first lands.

## TODO

- We don't yet have a written rule for what happens to a departed
  customer's historical campaign data (separate from their CRM record).
  Ask Priya before assuming it should just be deleted alongside the CRM
  record — these might need different retention.
