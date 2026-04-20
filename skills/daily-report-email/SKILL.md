---
name: daily-report-email
description: Draft a daily/weekly status report email to a manager or team. Use whenever the user asks for help writing a daily report, end-of-day update, status email, progress email, or "日报"/"周报"/"邮件日报"/"给老板发邮件汇报". Also triggers when the user describes their day's work and says something like "write this up", "send this to my boss", "summarize for <manager>", or hands you a list of things they did and asks for an email. Default output is a ready-to-send email (To / Cc / Bcc / Subject / Body), not a standalone document — the user will paste it into their mail client.
---

# Daily Report Email Drafter

Your job is to help the user produce a send-ready email draft of their daily (or multi-day) status report. You are **not** generating the content of their day — that comes from the user. You are shaping what they tell you into a clear, structured report their manager can read in 30 seconds.

## Core principles

1. **Email-first.** The output is an email, not a memo or a standalone markdown document. Always produce To / Cc / Bcc / Subject / Body. If the user ever asks for a "daily report" without specifying format, assume email.

2. **Content belongs to the user. Structure belongs to you.** Don't invent accomplishments, decisions, blockers, or next steps. If a section has no material, say so — don't pad.

3. **The report is written for a busy manager.** Keep every bullet tight. Every bullet should either convey progress, a decision that might affect the manager, a blocker the manager may need to unblock, or a plan the manager may want to redirect. No filler.

4. **Be deliberate about recipients.** Managers care a lot about who is Cc'd and Bcc'd on status updates — it signals scope and political awareness. Never guess. Always confirm before drafting.

## Step 1: Clarify recipients before drafting

Before producing any draft, check that you know:

- **To**: the primary recipient (usually the direct manager).
- **Cc**: anyone who should see it but isn't the target audience (skip-level, collaborators, peer leads).
- **Bcc**: anyone who should see it silently (often a skip-level or a personal archive).

If any of these are ambiguous or missing, **ask before drafting**. A good question looks like:

> "Before I draft: who should this go to? I'd assume <Manager> is the primary. Should I Cc anyone — e.g. your skip-level, or the PM on the project? Bcc?"

Do **not** invent recipient names. If the user has referenced a manager by name earlier in the conversation, you can propose that name back, but confirm Cc/Bcc explicitly.

The only time you can skip this step is if the user has already given you a complete recipient list in the current message (e.g. "send it to Jack, cc Lisa, bcc myself").

## Step 2: Collect the raw material

The user will usually give you a dump of what they did. Sort that material into four buckets:

- **Done** — things shipped, finished, or materially progressed today (or across the period).
- **Key Decisions** — choices made today that the manager might want visibility on or might want to push back on.
- **Blockers** — things stuck, especially anything requiring the manager's authority, a budget call, an external unblock, or a permission grant.
- **Next** — what the user will focus on next. Can include carryover from prior reports as well as new items.

If the user's dump is missing a bucket, **ask** rather than inventing it. A natural ask:

> "Anything blocking you right now, or should I leave the Blockers section out? And what's the plan for the next day or two?"

If the user tells you a bucket is genuinely empty (e.g. "no blockers today"), it's fine to omit that section from the draft. Don't force an empty "Blockers: none" line just to fill the template.

## Step 3: Draft the email

Use this structure. Follow it closely — it reflects what the user's manager expects to see.

```
To: <primary recipient>
Cc: <comma-separated, or leave blank>
Bcc: <comma-separated, or leave blank>
Subject: Daily Report – <Name> – <Date or Date Range>

Hi <Manager first name>,

<One-sentence framing: what period this covers and the overall theme of the work. Keep to one line.>

**Done**

- <Item>: <one-line summary of what happened and the core progress>. <ETA or completion status if relevant>
- ...

**Key Decisions**

- <Decision>: <background — why this came up>. <Rationale — why this choice>. <Tradeoff — what was given up or the main risk>
- ...

**Blockers**

- <Blocker>: <what's stuck and which project it blocks>. <What's needed — and from whom, especially if manager action is required>
- ...

**Next**

- <Upcoming item>: <brief>. <Why now, if it's new>
- ...

Thanks,
<User's name>
```

### Rules for each section

**Done bullets** should answer three questions in one line: *What did you do? How far did it get? When will it land (if not already)?*

- Good: `Finished the onboard wizard (12 steps, end-to-end works locally). Ready for Danny to smoke-test tomorrow.`
- Bad: `Worked on onboard wizard.` (no progress, no ETA)
- Bad: `Spent 6 hours debugging a weird httplib2 thing with proxies in containers on Tuesday and then on Wednesday I finally realized the fix was just to add PySocks as a dependency which is obvious in retrospect but took a while to isolate.` (too long — the manager doesn't need the detective story, just the resolution)

**Key Decision bullets** should expose the *why*, not just the *what*. A decision without context is just a fact; a decision with context lets the manager decide whether to push back. Structure as: decision → background → rationale → tradeoff/con. Keep it to one or two sentences, not a paragraph.

- Good: `Moved Ollama from inside the container to the host — Docker on Apple Silicon can't pass through the GPU, so in-container inference was 25x slower. Tradeoff: users now install Ollama separately, but the install script handles it.`
- Bad: `Moved Ollama to the host.` (no why — manager can't evaluate)

**Blocker bullets** should make it unambiguous whether *the manager* needs to act. If yes, say so explicitly. Managers scan this section for things they own.

- Good: `GHCR package is still private — needs to be made public for distribution. **Requires your action** — only you have package admin permissions for the org.`
- Bad: `Can't distribute the image yet.` (doesn't say why, doesn't say who can fix it)

**Next bullets** should be specific enough that the manager could redirect you if they disagreed with the priority. "Keep working on the wizard" is too vague; "Finish the wizard backfill step and hand to Danny for testing" is redirectable.

## Step 4: Output format

Produce the email as a single code block or clearly-delimited block that the user can copy-paste directly into their mail client. Do **not** wrap it in prose like "Here's the draft:" followed by commentary — the user wants to grab and go. A short one-line intro ("Draft below — let me know if you want anyone else Cc'd.") is fine, but the email itself should be clean.

If the user has given you their name earlier in the conversation, use it in the Subject and sign-off. Otherwise ask.

## Step 5: Offer revisions, don't argue

After the draft, invite the user to redirect: tone, length, section ordering, which items to cut. A daily report is a personal artifact — the user knows their manager's taste better than you do. If they say "this is too long, cut it in half," cut it in half without negotiating.

## On language

Default to English for the draft. If the user writes to you in Chinese, you can respond in Chinese *around* the draft (clarifying questions, summary) but the email body itself should be English unless the user explicitly asks for Chinese.

## On dates

If the user says "today" or "this week", convert to the absolute date using the current date from your context so the Subject line is unambiguous (e.g. `Daily Report – <Name> – April 17–19, 2026`).

## Example interaction

**User:**
> Write me a daily report. Today I finished the login page, decided to use NextAuth instead of building custom auth (simpler but locks us into their session model), and I'm blocked because I don't have access to the staging DB yet.

**You:**
> Before I draft: who's this going to? Primary recipient, plus anyone to Cc or Bcc?

**User:**
> To Jack, Cc Lisa (PM).

**You:**

> Draft below — let me know if you want anything cut or reworded.

```
To: Jack
Cc: Lisa
Subject: Daily Report – <Name> – <Today's Date>

Hi Jack,

Quick update on today's progress.

**Done**

- Login page: finished, end-to-end flow works locally. Ready for review.

**Key Decisions**

- Chose NextAuth over custom auth — simpler to ship and well-maintained. Tradeoff: we're locked into their session model, which may constrain us if we later need custom session logic.

**Blockers**

- No access to the staging DB yet — blocking end-to-end testing of the login flow. **Need your help** getting me added to the staging access group.

**Next**

- Wire up the signup page once staging access is sorted.
- Start on the forgot-password flow.

Thanks,
<Name>
```
