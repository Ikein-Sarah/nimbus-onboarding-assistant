---
title: Security Policy
department: general
owner: all
effective: 2026-05-01
summary: Account security, device rules, data handling, incident reporting and what happens if something goes wrong.
---

# Security Policy

Last updated by: daniel@nimbuslabs.io, reviewed by People and Finance leads.

This is the longest policy doc in the general folder on purpose — security
touches every department differently, so this page tries to cover all of
it in one place rather than scattering half-rules across department
folders. If you only read one section, read "Reporting a security
incident" at the bottom.

## 1. Account security

### 1.1 Passwords and the password manager

All credentials must live in 1Password. This is restated from
`it-setup.md` because it's the single most violated rule we see in audits
— people still paste API keys into Slack DMs "just for a second." Don't.
Slack messages are searchable company-wide by anyone with admin access,
and DMs are not an exception.

### 1.2 Two-factor authentication

2FA is mandatory on every account that supports it: email, Slack, GitHub,
the CRM, the accounting system, cloud consoles. Use an authenticator app
(1Password's built-in TOTP is fine) — not SMS. SMS-based 2FA is
disallowed for any system that touches customer data or money, because SIM
swap fraud has become common enough that it's not worth the residual risk.

### 1.3 Session and device locking

Lock your screen when you step away, even at home if you share space with
others. Laptops auto-lock after 10 minutes of inactivity company-wide —
this is enforced by device management, not optional.

### 1.4 Account creation and removal

Accounts are created as part of onboarding (see
`new-hire-first-week.md` and the department-specific onboarding
checklists) and removed as part of offboarding
(`people/offboarding-process.md`). Nobody should have standing access to
a system tied to a role they no longer hold — if you change teams
internally, your old department's access should be reviewed and trimmed,
not just left in place "in case." This doesn't happen automatically
today; flag it to your new manager if you notice it wasn't done.

### 1.5 Shared and service accounts

A small number of systems use shared logins rather than individual
accounts (a couple of the ad platforms, the physical office access
system where one exists). Shared credentials still live in a 1Password
shared vault, never in a personal password manager or a sticky note.
Anyone who no longer needs access to a shared account should be removed
from that vault, not just asked to "stop using it."

## 2. Device rules

### 2.1 Company laptops

- Only use your company laptop for company work where reasonably possible.
  Personal use (checking personal email, etc.) is fine; running a side
  business off it is not.
- Do not disable the endpoint security agent. If it's slowing your machine
  down, file a ticket — don't uninstall it.
- Full disk encryption is on by default and must stay on.

### 2.2 Personal devices

Personal devices may access email and Slack (mobile only) without extra
approval. Personal devices may **not** access the production database,
the accounting system, or the CRM's export features. This is a change
from an earlier, unwritten practice where a few people used personal
laptops for CRM work — that's no longer allowed as of this policy's
effective date, even if you were doing it before.

### 2.3 Lost or stolen devices

Report within 1 hour of noticing, to your manager and to IT via
#it-requests marked urgent. Do not wait until you're sure it's actually
lost — false alarms are free, delayed reports are not. Devices are remote
wiped as soon as the report is confirmed.

### 2.4 Travel with company devices

If you're traveling internationally with a company laptop, especially
somewhere your device could be inspected at a border, tell IT beforehand
via #it-requests. There's no blanket restriction on where you can travel
with company equipment, but a heads-up means IT can flag anything
unusual faster if the device later shows odd behavior. This is separate
from the working-from-abroad approval in
`hybrid-work-policy.md` — that's about employment and tax rules, this is
about device security, and you may need to think about both for the same
trip without one covering the other.

### 2.5 Physical security

For teams with an anchor day (`hybrid-work-policy.md`) meeting at a
shared space, the same device rules apply as anywhere else — don't leave
a laptop unattended and unlocked, even briefly, even among colleagues.
Most incidents involving a physically compromised device happen through
carelessness in a public or semi-public space, not theft from a locked
office.

## 3. Data handling

### 3.1 Customer data

Customer data lives in the CRM and the production database only. Do not
export customer lists to personal drives, personal email, or spreadsheets
outside the company Google Workspace. This restates and slightly extends
`growth/crm-rules.md`, which is Growth-specific; this section applies to
every department that touches customer data, including Engineering during
debugging and Finance during invoicing disputes.

### 3.2 Confidential internal data

Salary bands, individual compensation, unreleased product plans, and
performance review content are confidential. This is the same boundary
`code-of-conduct.md` describes at a high level — this section exists to
spell out the mechanism: confidentiality here means folder-level access
control (see `employee-handbook.md`, "Document access"), not just a
social norm. If you can technically read something you don't think you
should have access to, tell People — don't just quietly use it.

### 3.3 Data retention

- Rejected candidate records: 12 months, then deleted (see
  `people/hiring-process.md`).
- Customer deletion requests: completed within 30 days of request
  (see `growth/crm-rules.md`).
- Incident postmortems: kept indefinitely, redacted of any customer PII
  before wider circulation if needed.
- Slack message history: governed by the workspace-wide retention setting,
  currently 1 year. This is a platform setting, not something any
  individual can change per-channel.

## 4. Third-party tools and vendors

Before connecting a new SaaS tool to company data (OAuth-ing a tool into
Google Workspace, Slack, or the CRM counts as "connecting"), check with IT
first via #it-requests. This is separate from the procurement approval
process in `finance/procurement-approvals.md` — procurement approves the
spend, this approves the data access, and you may need both. A tool can be
under the no-approval spending threshold and still need a security review
if it touches customer data (see the "New vendors" section of
`finance/procurement-approvals.md`, which mentions this in passing).

## 5. Reporting a security incident

If you suspect a security incident — a compromised account, a phishing
email that someone clicked, unexpected access to something, unusual
production behavior that might be an intrusion rather than a bug — report
it immediately:

1. Post in #security-incidents (not the general engineering or incident
   channel — this one is more restricted and monitored specifically for
   this).
2. Tag your manager and Daniel Osei (Engineering Manager) directly, even
   outside working hours if it looks serious.
3. Do not try to "fix it quietly" first. Early containment steps taken by
   someone unfamiliar with the specific system can destroy evidence needed
   to understand what happened.

A security incident is handled differently from a production incident.
Compare with `engineering/oncall-rotation.md`, which covers Sev1-Sev3
production incidents — those go through the normal on-call escalation.
Security incidents skip that path entirely and go straight to
#security-incidents regardless of severity, because the response steps
are different (containment and forensics, not just restoring service).

## 6. What happens after a report

- Someone acknowledges your report within 30 minutes during working hours,
  2 hours outside working hours.
- A short internal postmortem is written within 5 working days, following
  roughly the same blameless format as `engineering/incident-postmortem-2026-03-outage.md`,
  adapted for security specifics.
- If customer data was affected, Legal and the CEO are looped in before any
  customer communication goes out. Nobody messages a customer about a
  security issue unilaterally.

## 7. A worked example

To make sections 5 and 6 concrete: suppose someone clicks a phishing
link that looks like a Google Workspace login page and enters their
password. Here's what the process actually looks like end to end:

1. They notice something felt off (the page looked slightly wrong) and
   post in #security-incidents immediately, per section 5, even though
   they're not fully sure anything happened.
2. Someone acknowledges within 30 minutes (working hours) per section 6,
   and asks them to change their Google Workspace password immediately
   and check for any unfamiliar login locations in their account
   activity.
3. Because 2FA was enabled (section 1.2), the attacker likely couldn't
   complete a login even with the password — this is the main reason 2FA
   is non-negotiable company-wide, not just a compliance checkbox.
4. IT reviews recent account activity for anything unusual. If nothing
   unusual is found, the incident is closed with a short note; if
   something is found, it escalates into the fuller containment process.
5. A short postmortem is written within 5 working days per section 6,
   blameless per the same principle as engineering incident reviews
   (`engineering/oncall-rotation.md`) — the person who clicked the link
   is not the subject of the writeup, the phishing pattern and the
   response process are.

This is deliberately a "nothing bad happened" example. Most security
incident reports resolve this way — reporting is cheap, not reporting is
the expensive failure mode.

## 8. Annual review

This policy is reviewed annually, every May, or sooner if a real incident
surfaces a gap. Last substantive change: the personal-device restriction
in section 2.2, added this cycle after an internal audit.

## 8a. Frequently misunderstood parts of this policy

A few things People and IT get asked about repeatedly, worth clarifying
directly:

- **"Does 2FA on my personal accounts count?"** No — 2FA requirements in
  section 1.2 apply to Nimbus Labs accounts specifically. What you do on
  personal accounts is your own business, though obviously also a good
  idea.
- **"If my device is encrypted, do I still need to lock my screen?"**
  Yes. Encryption protects data if the device is powered off and stolen;
  it does nothing if someone sits down at an unlocked, running laptop.
  These are different threats and section 1.3's screen-lock rule exists
  for the second one.
- **"Is reporting a false alarm going to get me in trouble?"** No,
  explicitly not — section 2.3 says this directly for lost devices, and
  the same principle holds for section 5's incident reporting. The cost
  asymmetry (cheap false alarms vs. expensive missed real incidents) is
  the whole reason the bar for reporting is set low.
- **"Can I use a personal password manager instead of 1Password?"** No —
  section 1.1's requirement is specifically the company's 1Password
  instance, not "a password manager of your choice." This is partly
  about consistency and partly about the company's ability to revoke
  access to shared vaults on offboarding, which only works if everyone's
  actually using the same tool.

## 9. Questions this policy doesn't answer

A few things intentionally live elsewhere rather than being duplicated
here:

- Who specifically approves a new tool's data access — see
  `tooling-and-access-requests.md` for the request mechanics; this
  document covers the principle (check with IT, get a security review if
  customer data is involved) but not the day-to-day approval workflow.
- What happens to a departing employee's access — that's
  `people/offboarding-process.md` in full; this document only states the
  general retention principles in section 3.3.
- Engineering-specific production access rules (who can touch the
  database, who's on the deploy pipeline) — see
  `engineering/architecture-overview.md` and
  `engineering/oncall-rotation.md`. This policy sets the baseline that
  those documents build on, not a replacement for them.
