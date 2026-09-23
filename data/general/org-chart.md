---
title: Org Chart
department: general
owner: all
effective: 2026-09-01
summary: Reporting lines, department leads and how the four departments fit together.
---

# Org Chart

Last updated by: tunde@nimbuslabs.io (People). If your reporting line
changed and this page hasn't caught up, tell People directly — Workday is
always the source of truth, this page just makes it readable.

## Leadership

Nimbus Labs was co-founded in 2021 by Ifeoma Chukwu (CEO) and one other
co-founder who is no longer with the company. Ifeoma sits above all four
departments and is the final approver referenced in
`finance/budget-planning.md` and `finance/procurement-approvals.md`.

## Departments

```
Ifeoma Chukwu (CEO)
├── Daniel Osei — Engineering Manager
│   ├── John Adeyemi — Senior Engineer (Tech Lead)
│   ├── Sarah Ikein — AI Engineer
│   └── (6 more engineers, not in the demo roster)
├── Priya Raman — Head of Growth
│   └── Amaka Eze — Growth Manager
│       └── (growth team, not in the demo roster)
├── Tunde Bello — People Partner
│   └── (People team)
└── Henrik Larsen — Finance Lead
    └── Lara Mensah — Finance Analyst
```

## Notes on the chart above

- This is deliberately simplified. The demo user set
  (`users.seed.json`) only has 8 people; the real company has 84. Don't
  assume anyone not listed here doesn't exist — assume the chart is
  incomplete for anyone below manager level.
- Engineering is the largest department (roughly 35 people company-wide),
  followed by Growth, then Finance, then People.
- "Department lead" in `finance/procurement-approvals.md` means the person
  at the top of each branch above: Daniel for Engineering, Priya for
  Growth, Tunde for People, Henrik for Finance.
- The People department and the "People team" mentioned throughout the
  handbook are the same thing. Same for "Finance team" / Finance department.

## Who approves what (quick cross-reference)

| Decision | Approver | Source doc |
|---|---|---|
| Leave request | Your manager | `general/leave-policy.md` |
| Expense under limit | Auto-approved | `finance/expense-policy.md` |
| Campaign spend over 5,000 USD | Growth lead + Finance | `growth/campaign-process.md` |
| Vendor contract over 25,000 USD/yr | Finance lead + CEO | `finance/procurement-approvals.md` |
| Offer above band midpoint | Finance | `people/hiring-process.md` |

## TODO

- Add a real org chart image once we're off ASCII art. Someone file a
  design request with Growth for this.
- Confirm whether the second co-founder should be named here at all —
  checking with Ifeoma first.
