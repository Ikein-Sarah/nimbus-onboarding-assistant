---
title: Nimbus Labs Employee Handbook
department: general
owner: all
effective: 2026-01-01
summary: Company overview, values, working hours and general expectations for all staff.
---

# Nimbus Labs Employee Handbook

Last updated by: tunde@nimbuslabs.io. This is the longest-running doc in
the company wiki and the one most likely to drift out of date in small
ways — if a section here disagrees with a more specific, more recently
dated doc, follow the specific one and flag the gap to People.

## About Nimbus Labs

Nimbus Labs builds workflow automation software for mid-sized logistics
companies. We were founded in 2021 and now have 84 employees across four
departments: Engineering, Growth, People, and Finance. (`general/` itself
isn't a department you can be hired into — it's just where company-wide
documents live.)

### History and values

Nimbus Labs started as a two-person project automating dispatch scheduling
for a single freight customer in Lagos. The founding insight was simple:
logistics companies were running critical workflows in a tangle of
spreadsheets, WhatsApp groups, and phone calls, and the software built for
enterprise logistics was too heavy and too expensive for the mid-market.
Nimbus Flow, the product, grew out of that first dispatch tool.

The company has stayed intentionally mid-sized. We are not chasing
headcount for its own sake, and growth in employee count has historically
tracked customer growth rather than running ahead of it. That's part of
why the org chart (`org-chart.md`) still fits on one page even at 84
people.

Three things we say out loud often enough that new joiners should hear
them explicitly:

1. **Plain over clever.** This shows up in the product (see the "Voice"
   section of `growth/brand-guidelines.md`) and in how we write internal
   docs. If a document needs a glossary to be understood, something's
   wrong with the document, not just the reader — which is part of why
   `glossary.md` exists, as a patch, not a permanent fixture.
2. **Blameless, not consequence-free.** Incident reviews
   (`engineering/oncall-rotation.md`) and performance conversations
   (`people/performance-review-cycle-2026.md`) both start from "what
   happened and why," not "whose fault was it." That doesn't mean
   outcomes don't matter — it means we fix the system before we fix the
   person.
3. **Say the number, even when it's bad.** Borrowed directly from
   `growth/campaign-process.md`'s measurement section, but it applies
   company-wide: report the real metric, not the flattering one.

### What we don't have (yet)

To set expectations early: there's no employee stock option program and
no company pension scheme. See `faq.md` for the informal version of this
answer, since it comes up constantly from candidates and new joiners.

### How this handbook relates to the rest of the wiki

This document is deliberately broad and, in places, deliberately
shallow — it's meant to be readable in one sitting on someone's first
day, not to be the authoritative source on any single topic. Where a
more specific document exists, that document wins if the two ever
disagree, per the dating principle above. A rough mental model:

- This handbook: "what kind of company is this, and what do I need to
  know in week one."
- Department folders: "how does my team actually do its work."
- `general/faq.md` and `general/glossary.md`: "quick, informal answers
  to specific questions."
- Personal folders: "what's true about me, specifically."

### A note on tone

You'll notice this handbook, and most of the general-folder documents,
read fairly plainly — short sentences, direct statements, not much
corporate hedging. That's intentional and matches the "plain over
clever" value above. Department docs vary more: Engineering docs tend to
be terser and more procedural, Growth docs a little warmer and more
conversational, Finance docs more formal, People docs somewhere in
between. None of this is enforced top-down; it's just how each
department's writers naturally write, and nobody's tried to homogenize
it.

### How the company is organized

Four departments, each with its own lead at the top of the branch in
`org-chart.md`: Engineering (Daniel Osei), Growth (Priya Raman), People
(Tunde Bello), Finance (Henrik Larsen). All four report to the CEO.
Engineering is the largest department by headcount, which shapes some of
the language in this handbook — a few sections below lean on engineering
examples simply because that's where most people work, not because
engineering matters more than the other three.

Nimbus Flow itself is described in more technical depth in
`engineering/architecture-overview.md` if you want to understand what the
product actually does under the hood; this handbook only covers the
company side.

### A short note on how documents are dated

Every document in this wiki carries an `effective` date in its header.
When two documents disagree, the one with the later effective date is
current — this is how the "superseded" pattern works throughout the
corpus (see `hybrid-work-policy.md` superseding `remote-work-policy.md`,
or `deployment-process-v2.md` superseding `deployment-process.md`). If
you're ever unsure which of two conflicting documents to trust, check the
dates before asking someone.

## Working hours

Core hours are 10:00 to 16:00 in your local time zone. Outside core hours
you manage your own schedule. All employees are expected to be reachable
on Slack during core hours. See `meeting-norms.md` for how this interacts
with scheduling meetings across time zones.

### Time zones in practice

Nimbus Labs has never been a single-timezone company — the founding team
itself split across Lagos and a couple of European cities early on, and
that pattern held as the company grew. Practically, this means:

- Your manager should know your core hours, not assume they match theirs.
- Cross-timezone meetings should land in the overlap of both people's
  core hours, per `meeting-norms.md` — if there's no overlap, prefer
  async.
- "Reachable on Slack" doesn't mean "responds instantly." It means you'll
  see and respond to something within your working day, not that you're
  glued to the app.

## Your first week

Short version, for quick reference:

- Day 1: accounts, laptop setup, and a welcome call with your manager.
- Day 2 to 3: read your department onboarding docs and meet your team.
- Day 4 to 5: pair with a buddy on a small starter task.

This summary hasn't been rewritten in a while. For the actual day-by-day
checklist with the specifics that matter (like the 400 USD stipend
deadline and the security read requirement), use
`new-hire-first-week.md` instead — it's maintained more often than this
section is.

## Who to ask

Questions about pay, benefits, or leave go to the People team. Questions
about tools and access go to IT (in practice, post in #it-requests — see
`tooling-and-access-requests.md`). Anything you cannot place goes to your
manager first.

## Document access

Company documents are grouped by department. You can read general
documents, the documents for your own department, and your own personal
records. You cannot read other departments' internal documents or another
employee's personal records — this holds even within the same department;
being on the same team as someone does not give you access to their
personal folder.

### The one exception worth knowing about

Performance review notes are the one document type that isn't strictly
owner-only within a personal folder: `people/performance-review-process.md`
states that review notes are visible to the employee, their manager, and
the People team. That's a narrow, explicit carve-out for that one
document type — it doesn't extend to offer letters or equipment records,
which stay owner-only even from your own manager.

### Why access is scoped this way

This isn't just a technical default — it's meant to match how the
company actually thinks about information. Department-restricted
documents (salary bands, budget plans, campaign strategy) usually contain
numbers or plans that aren't finished or aren't everyone's business yet.
General documents are things every employee needs regardless of role.
Personal documents are, straightforwardly, personal. If you ever find you
can technically read something that seems like it should be out of
reach, that's worth reporting — see `security-policy.md` section 3.2.

## Where things live, at a glance

| You want to know about... | Start here |
|---|---|
| Who reports to whom | `org-chart.md` |
| What a term means | `glossary.md` |
| An unwritten question | `faq.md` |
| Meeting culture | `meeting-norms.md` |
| Keeping accounts and devices secure | `security-policy.md` |
| Requesting a new tool | `tooling-and-access-requests.md` |
| How levels and promotions work | `people/career-levels-and-promotion.md` |
| How the product is built | `engineering/architecture-overview.md` |
| Your first week, in detail | `new-hire-first-week.md` |

## What "general" means, precisely

Worth being precise about this since it's foundational to how the whole
document access model works: `general/` is not a department. Nobody has
`general` as their `role` in `users.seed.json`, and there's no "general
team" you could be hired into. It's a folder of documents that every
employee, regardless of department, can read — this handbook is one, so
are `code-of-conduct.md`, `leave-policy.md`, `security-policy.md`, and
the rest of the folder. When a document says "readable by everyone," this
folder is what that means in practice.

## Values in practice — a couple of real examples

Values statements are easy to write and easy to ignore, so it's worth
pointing at where these actually showed up in real documents rather than
just asserting them:

- **Blameless, not consequence-free** shows up concretely in
  `engineering/incident-postmortem-2026-03-outage.md`, which never names
  the on-call engineer involved, and in
  `people/performance-review-process.md`'s confidentiality rule, which
  keeps review conversations narrowly scoped rather than broadcast.
- **Say the number, even when it's bad** shows up in
  `growth/campaign-process.md`'s measurement section, and again in this
  very corpus's own honesty about gaps — several documents in this wiki
  include a TODO section admitting what isn't finished yet, rather than
  pretending every process is fully buttoned up. `general/it-setup.md`
  and `general/tooling-and-access-requests.md` both say plainly that
  they don't have a dedicated owner yet, for instance.
- **Plain over clever** is easiest to see by contrast: compare the tone
  of this handbook to a typical enterprise policy document. Short
  sentences, concrete examples, minimal jargon (and where jargon is
  unavoidable, `glossary.md` exists specifically to catch it).

## Revision history (informal)

This handbook doesn't have a formal changelog, but a few landmark
changes are worth knowing about if you're trying to make sense of an old
reference to it: the "Your first week" section used to be the
authoritative onboarding checklist before `new-hire-first-week.md` was
split out as its own, more detailed document. If you find an old export
or printout of this handbook that still has a long onboarding section,
it predates that split — treat `new-hire-first-week.md` as current.
