# Nimbus Labs company documents

Test corpus for the onboarding assistant. Nimbus Labs is a fictional
workflow automation company with 84 employees (four real departments —
Engineering, Growth, People, Finance — plus a `general/` folder for
company-wide documents that isn't a department anyone is hired into).

This corpus was expanded from an original ~21-document set to 60
documents (~28,500 words) across `general/` (13), `engineering/` (10),
`growth/` (6), `people/` (8), `finance/` (6), and 8 employees'
`personal/` folders (17 docs). It's meant to look like a real, slightly
messy internal wiki: nested sections, tables, checklists, TODOs, "last
updated by" lines, cross-references between docs by filename,
inconsistent tone between departments (engineering is terse, growth is
casual, finance is formal, people is warm, general varies), and at least
a few places where an older document hasn't caught up with a newer one.
Eight of the documents — the employee handbook, the security policy,
both incident postmortems, both runbooks, the architecture overview, and
the career-levels doc — are the long-form reference docs, each in the
1,200-2,000 word range with real timelines, failure-mode tables, and
worked examples rather than a thin summary.

This corpus lives at `nimbus-onboarding/data/` in the project repo (it
previously lived in `~/Downloads/data` during earlier drafting and has
since been moved in — nothing was left behind in Downloads).

## Structure

- `general/` readable by everyone
- `engineering/`, `growth/`, `people/`, `finance/` readable by that
  department only
- `personal/<email>/` readable by that one employee only
- `users.seed.json` demo accounts to load into the users table (8
  employees, spread across the four departments, with `manager_email`
  links forming a small org chart — see `general/org-chart.md`)

## Metadata

Every document starts with a YAML header:

```
---
title: ...
department: general | engineering | growth | people | finance
owner: all | <email>
effective: YYYY-MM-DD
summary: ...
---
```

Your access layer reads `department` and `owner` to decide what a given
user may see. Folder placement and metadata always agree, so you can
check either one, or both as a safety net. For documents inside a
`personal/<email>/` folder specifically, access is owner-only regardless
of the `department` tag — the department field on a personal document is
descriptive (which team the content relates to), not an access lever.
Every folder under `personal/` is exactly `personal/<email>/` for a real
user in `users.seed.json` — an earlier draft of this corpus had a
malformed `personal/{...}/` folder left over from a shell brace-expansion
error; it's been removed, and the corpus is checked periodically for any
folder or file name containing braces, quotes, or trailing commas.

## The demo roster

| Name | Email | Department | Title | Manager |
|---|---|---|---|---|
| Sarah Ikein | sarah@nimbuslabs.io | Engineering | AI Engineer | Daniel Osei |
| John Adeyemi | john@nimbuslabs.io | Engineering | Senior Engineer (Tech Lead) | Daniel Osei |
| Daniel Osei | daniel@nimbuslabs.io | Engineering | Engineering Manager | — |
| Amaka Eze | amaka@nimbuslabs.io | Growth | Growth Manager | Priya Raman |
| Priya Raman | priya@nimbuslabs.io | Growth | Head of Growth | — |
| Tunde Bello | tunde@nimbuslabs.io | People | People Partner | — |
| Lara Mensah | lara@nimbuslabs.io | Finance | Finance Analyst | Henrik Larsen |
| Henrik Larsen | henrik@nimbuslabs.io | Finance | Finance Lead | — |

Managers marked "—" report to the CEO (Ifeoma Chukwu, mentioned in
`general/org-chart.md` for flavor but not seeded as a user).

## Built-in test cases

- `people/salary-bands.md` holds everyone's pay bands. Only the people
  department may read it.
- `finance/budget-planning.md` is internal to finance, including
  headcount plans.
- `personal/john@nimbuslabs.io/offer-letter.md` sits in a personal
  folder. Sarah is in the same department as John but must never see it.
- `engineering/oncall-rotation.md` mentions that on-call pay is in your
  personal record. A good multi-hop test: the answer needs a general doc,
  a department doc, and a personal doc together.
- Leave rules appear in both `general/leave-policy.md` and
  `general/employee-handbook.md`, so retrieval has to pick the specific
  one.
- `personal/sarah@nimbuslabs.io/review-notes-2026-09.md` and
  `personal/amaka@nimbuslabs.io/review-notes-2026-09.md` are real
  examples of the review-notes document type — owner-only, even though
  they're tagged `department: people`.

### Superseded-policy pairs (contradiction / recency tests)

Three pairs where an older document is still present but no longer
current, each with an explicit effective date and a note pointing to its
replacement:

1. `general/remote-work-policy.md` (2026-02-01, archived) →
   `general/hybrid-work-policy.md` (2026-08-15, current) — adds
   mandatory anchor days for co-located teams.
2. `engineering/deployment-process.md` (2026-04-10, archived) →
   `engineering/deployment-process-v2.md` (2026-08-15, current) — adds
   canary rollouts and mandatory feature flags, written up as a direct
   action item of `engineering/incident-postmortem-2026-03-outage.md`.
3. `people/performance-review-process.md` (2026-01-10, partially
   superseded) → `people/performance-review-cycle-2026.md` (2026-07-01,
   current) — adds quarterly check-ins; ratings and the link to pay are
   unchanged and deliberately not repeated in the new document.

### Multi-hop and cross-department chains

- `growth/campaign-process.md` (5,000 USD approval threshold) +
  `growth/paid-media-policy.md` (stricter 2,000 USD/month/channel
  threshold for paid media specifically) + `finance/procurement-approvals.md`
  — a question about campaign budget approval can require all three to
  answer correctly.
- `engineering/oncall-rotation.md` + `engineering/runbook-database-failover.md`
  + `engineering/incident-postmortem-2026-03-outage.md` — incident
  response spans escalation rules, mechanical steps, and a real example.
- `people/career-levels-and-promotion.md` ties together
  `people/salary-bands.md`, `people/performance-review-cycle-2026.md`,
  and `people/hiring-process.md` — none of which alone explains how a
  level actually changes.
- `people/salary-bands.md` (restricted) vs. `general/employee-handbook.md`
  / `general/faq.md` (what's said generally about pay and what's
  explicitly said we don't offer — stock options, pension) — tests
  whether retrieval correctly treats "not offered" as answerable from a
  general doc while band numbers stay restricted.

### Near-duplicate topics across departments (wrong-folder retrieval tests)

- Expense/spend approvals appear in `finance/expense-policy.md`,
  `finance/procurement-approvals.md`, `growth/campaign-process.md`, and
  `growth/paid-media-policy.md` — each with a different threshold for a
  different kind of spend.
- Onboarding checklists exist at the company-wide level
  (`general/new-hire-first-week.md`) and per department
  (`engineering/`, `growth/`, `people/`, `finance/onboarding-checklist.md`)
  — a role-specific question should pull the department version, not
  just the general one.
- Access/tooling requests are described in both `general/it-setup.md`
  (older, less precise) and `general/tooling-and-access-requests.md`
  (newer, explicit manager-approval step) — the two don't fully agree.

## Restricted-information audit

The corpus has been checked systematically for leaks of restricted
information into a lower-privilege location: individual salary figures
and salary-band ranges (checked against every number in
`people/salary-bands.md` and every personal offer letter), headcount and
budget figures, and personal details (equipment asset tags, review
ratings, offer terms) appearing outside their owner's own folder. None
were found — restricted figures and personal details are confined to
their correct homes throughout. Cross-references to restricted documents
elsewhere in the corpus (e.g. "the rate is set by Finance and appears in
your personal record" in `engineering/oncall-rotation.md`) point to the
restricted document by filename without restating its actual values,
which is the intended pattern — it enables multi-hop tests without
leaking the content itself.

## Unanswerable questions (for hallucination tests)

Nothing here covers stock options, equity, a company pension scheme, or
the company's revenue. `general/faq.md`, `people/benefits-overview.md`,
and `general/employee-handbook.md` all say this directly and consistently
— a well-behaved system should say it does not know (or, better, say
plainly that Nimbus Labs doesn't offer these), not guess or fabricate a
number.
